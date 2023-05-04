import uuid
from django.utils import timezone
from django.db import models


class Category(models.Model):
    """
    id(PK): category 아이디 (ex: recent)
    name: category 이름 (ex: 최신)
    url: 인기 급상승 해당 카테고리 링크
    videos: 인기 급상승 해당 카테고리 영상 목록 (video id 값)
    """
    id = models.CharField(max_length=32, primary_key=True, editable=False)
    name = models.CharField(max_length=32)
    url = models.URLField(max_length=200)
    videos = models.ManyToManyField('Video', through='Trending')

class Video(models.Model):
    """
    id(PK): 동영상 아이디
    title: 동영상 제목
    thumbnail: 썸네일 이미지 링크
    url: 동영상 링크
    count_of_views: 조회 수
    count_of_comments: 댓글 수
    categories: 연관된 인기 급상승 카테고리 목록
    """
    id = models.CharField(max_length=32, primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    thumbnail = models.URLField(max_length=200)
    url = models.URLField(max_length=200)
    count_of_views = models.PositiveBigIntegerField(default=0)
    count_of_comments = models.PositiveBigIntegerField(default=0)
    categories = models.ManyToManyField('Category', through='Trending')

class Comment(models.Model):
    """
    id(PK): uuid
    video: 연관된 video
    content: 댓글 내용
    count_of_thumbs: 좋아요 수
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, null=True)
    content = models.TextField(blank=True, null=True)
    count_of_thumbs = models.PositiveBigIntegerField(default=0)

class Tag(models.Model):
    """
    id(PK): uuid
    video: 연관된 video
    content: tag 내용
    created_date: 생성일
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.ForeignKey('Video', on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=32)
    created_date = models.DateTimeField(default=timezone.now)

class Trending(models.Model):
    """
    id(PK): uuid
    category: 연관된 category
    video: 연관된 video
    created_date: 생성일
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

class WordCloud(models.Model):
    """
    id(PK): uuid
    category: 연관된 category
    wordcloud: 이미지 경로
    created_date: 생성일
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    wordcloud = models.ImageField(upload_to ='images/')
    created_date = models.DateTimeField(default=timezone.now)