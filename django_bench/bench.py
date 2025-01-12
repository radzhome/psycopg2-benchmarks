#!/usr/bin/env python
from __future__ import print_function

import os
import sys

# Needed to run standalone django script
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.path.append('.')
import django
django.setup()

import random
from datetime import timedelta
from datetime import datetime

from db_app.models import Post
from django.contrib.auth.models import User
from utils import bulk_ids
from utils import measure_time

post_db_table = Post.objects.model._meta.db_table


def run_all(size):
    """ Run all benchmarks. Assumes empty DB
    """
    user_count = User.objects.all().count()
    assert user_count == 0
    assert Post.objects.all().count() == 0
    deco = measure_time  # (stat_profile=True)
    total_time = 0.0
    for create_fn in (bulk_insert, many_inserts, many_updates):
        total_time += deco(create_fn)(size)
    for select_fn in (many_selects, select_all,
                      # select_all_values_list, # measures the same as cursor_fetchall
                      cursor_fetchall):
        total_time += deco(select_fn)()
    print(f"Total time was {total_time}s")
    return total_time


def bulk_insert(size):
    """ Create a lot of object in bulk
    """
    n_objects = size
    now = datetime.now()
    user_list, post_list = [], []
    user_ids, post_ids = [bulk_ids(m, n_objects) for m in (User, Post)]
    for i, user_id, post_id in zip(
            range(1, n_objects + 1), user_ids, post_ids):
        user, post = new_user_post(i, now, 'bulk')
        user.id = user_id
        post.author = user
        user_list.append(user)
        post_list.append(post)
    User.objects.bulk_create(user_list)
    Post.objects.bulk_create(post_list)


def many_inserts(size):
    """ Create one object at a time
    """
    n_objects = size // 10
    now = datetime.now()
    user_list, post_list = [], []
    for i in range(n_objects):
        user, post = new_user_post(i, now, 'single')
        user.save()
        post.author = user
        post.save()


def many_updates(size):
    """ Update one object at a time
    """
    n_objects = size // 10
    now = datetime.now()
    for i, post in enumerate(Post.objects.all()[:n_objects]):
        post.created_at = now
        post.title += ' (2)'
        if i % 2:
            post.author = None
        post.save()


def select_all():
    """ Create a list with all objects
    """
    so_many_posts = []
    for _ in range(10):
        so_many_posts.extend(Post.objects.all())


def select_all_values_list():
    """ Get all objects with .values_list - less django overhead
    """
    so_many_posts = []
    for _ in range(20):
        so_many_posts.extend((Post.objects.all() \
                              .values_list('id', 'title', 'text', 'created_at')))


def cursor_fetchall():
    """ Get all objects with cursor.fetchall, without django
    """
    from django.db import connection
    cursor = connection.cursor()
    so_many_posts = []
    for _ in range(20):
        cursor.execute(f'select * from {post_db_table};')
        so_many_posts.extend(cursor.fetchall())
    return so_many_posts


def many_selects():
    """ Trigger queries by accessing ForeignKey field
    """
    posts = list(Post.objects.all())
    return [post.author for post in posts[: (len(posts) // 2)]]


def new_user_post(i, now, prefix):
    """ Create new User and Post instances without saving them
    """
    username = '%s user %d' % (prefix, i)
    dt = now - timedelta(seconds=random.randint(0, 1000))
    user = User(username=username)
    post = Post(
        title='A post by ' + username,
        text='a long long text' * 10,
        created_at=dt)
    return user, post


def cli():
    usage = 'usage: ./bench.py <job size> <number of runs>'
    if len(sys.argv) not in [2, 3]:
        sys.exit(usage)
    else:
        try:
            size = int(sys.argv[1])
            if len(sys.argv) == 3:
                warmup = int(sys.argv[2])
            else:
                warmup = 10
        except ValueError:
            sys.exit(usage)
        else:
            total_total_time = 0.0
            for _ in range(warmup):  # giving PyPY JIT time to warm up
                total_total_time += run_all(size)
                User.objects.all().delete()
                Post.objects.all().delete()
            print(f"Average time was {total_total_time / warmup}s, total total time was {total_total_time}s")


if __name__ == '__main__':
    cli()
