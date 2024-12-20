"""
This module contains serializers for the Article, Clap, Topic, and TopicFollow models.
"""
from rest_framework import serializers

from users.models import CustomUser
from users.serializers import AuthorSerializer
from .models import Article, Clap, Topic, TopicFollow


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for the Topic model."""

    class Meta:
        model = Topic
        fields = ["id", "name", "description", "is_active"]


class ClapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clap
        fields = [
            "id",
            "user",
            "article",
        ]


class ArticleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating articles."""
    author = AuthorSerializer(read_only=True)
    topics = TopicSerializer(read_only=True, many=True)
    topic_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Topic.objects.all(), write_only=True, source="topics"
    )
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "summary",
            "topics",
            "content",
            "status",
            "thumbnail",
            "author",
            "topic_ids",
            "created_at",
            "updated_at",
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    topics = TopicSerializer(many=True)
    claps = ClapSerializer(many=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "summary",
            "topics",
            "status",
            "content",
            "thumbnail",
            "author",
            "created_at",
            "updated_at",
            "claps",
            "views_count",
            "reads_count",
        ]


class ArticleListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    topics = TopicSerializer(many=True)
    claps = ClapSerializer(required=False, many=True, write_only=True)
    claps_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "summary",
            "topics",
            "status",
            "content",
            "thumbnail",
            "author",
            "created_at",
            "updated_at",
            "claps_count",
            "views_count",
            "reads_count",
            "claps",
        ]

    def get_claps_count(self, obj):
        return obj.claps.count()


class TopicFollowSerializer(serializers.ModelSerializer):
    """Serializer for the TopicFollow model."""

    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = TopicFollow
        fields = [
            "topic",
            "user",
        ]



