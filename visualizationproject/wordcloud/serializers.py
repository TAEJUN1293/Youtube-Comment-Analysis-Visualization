from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Video
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TrendingSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True, many=True)
    # video = VideoSerializer(read_only=True, many=True)
    class Meta:
            model = Trending
            fields = '__all__'


class WordCloudSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordCloud
        fields = '__all__'
