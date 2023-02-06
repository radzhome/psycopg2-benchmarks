from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField()
    author = models.ForeignKey('auth.User', null=True, on_delete=models.CASCADE)
