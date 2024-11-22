from rest_framework import serializers

from users.models import CustomUser
from users.serializers import AuthorSerializer

from .models import Article, Topic


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ["name", "description", "is_active"]


class ArticleCreateSerializer(serializers.ModelSerializer):
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

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "summary",
            "topics",
            "content",
            "thumbnail",
            "author",
            "created_at",
            "updated_at",
        ]
