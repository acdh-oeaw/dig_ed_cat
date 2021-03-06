from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class NewsFeed(models.Model):
    title = models.CharField(blank=True, max_length=250)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, related_name='blog_posts', on_delete=models.PROTECT
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return "{}".format(self.title)
