"""
This module provides API views for managing topics and articles.

Includes:
- TopicCreateAPIView: API view to create a new topic.
- ArticlesView: ViewSet for managing Article instances,
  providing full CRUD operations with filtering support.
"""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.response import Response

from articles.filters import ArticleFilter
from articles.models import Article, Topic
from articles.serializers import (
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    ArticleListSerializer,
    TopicSerializer,
)


class TopicCreateAPIView(generics.CreateAPIView):
    """
    API view to create a new topic.
    """
    queryset = Topic.objects.all() if hasattr(Topic, 'objects') else None
    serializer_class = TopicSerializer


# Create your views here.
class ArticlesView(viewsets.ModelViewSet):
    """
    ViewSet for managing Article instances, providing CRUD operations.
    """
    queryset = Article.objects.all() if hasattr(Article, 'objects') else None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter

    def get_serializer_class(self):
        if self.action == "create":
            return ArticleCreateSerializer
        if self.action == "retrieve":
            return ArticleDetailSerializer
        if self.action == "list":
            return ArticleListSerializer
        return ArticleCreateSerializer

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            return self.queryset.filter(status=Article.Status.PUBLISH)
        return super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            if self.request.user == instance.author:
                instance.status = "trash"
                instance.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(
            status=status.HTTP_403_FORBIDDEN, data={"detail": "Not authorized."}
        )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            if self.request.user == instance.author:
                serializer = self.get_serializer(
                    instance, data=request.data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)

            return Response(
                status=status.HTTP_403_FORBIDDEN, data={"detail": "Not authorized."}
            )

        return Response(status=status.HTTP_404_NOT_FOUND)
