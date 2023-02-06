Benchmark Python bindings for PostgreSQL using Django
=====================================================

This is a tiny django benchmark, that measures some common operations:

* creating objects in bulk (using ``model.objects.bulk_create``)
* creating objects one at a time
* updating objects one at a time
* querying objects one at a time (accessing ForeignKey field)
* selecting a lot of objects using ``model.objects.all``
* selecting a lot of objects using ``model.objects.all().values_list``
* selecting a lot of objects using ``cursor.fetchall``

The goal is not to measure the raw speed
of Postgres bindings, but to evaluate them in a way similar to the way
they are used in real-life web applications. Although ``cursor.fetchall``
benchmark does not use Django directly.

Install::

    pip install -r requirements.txt


Run::

    ./bench 1000

It will run the benchmark several times, to give PyPy JIT time to warm up.

See  ``settings.py``.
