import uuid
from django.utils import timezone
from django.db import models


class Category(models.Model):
    id = models.CharField(max_length=32, primary_key=True, editable=False)
    name = models.CharField(max_length=32)
    url = models.URLField(max_length=200)
    videos = models.ManyToManyField('Video', through='Trending')

class Video(models.Model):
    id = models.CharField(max_length=32, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    thumbnail = models.URLField(max_length=200)
    url = models.URLField(max_length=200)
    count_of_views = models.PositiveBigIntegerField(default=0)
    count_of_comments = models.PositiveBigIntegerField(default=0)
    categories = models.ManyToManyField('Category', through='Trending')

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, null=True)
    content = models.TextField(blank=True, null=True)

class Trending(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)