from django.db import models


class Video(models.Model):
    data = models.JSONField(default='{}')
    class Meta:
        db_table = "videos"


