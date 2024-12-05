"""
This module provides API views for managing topics and articles.

Includes:
- TopicCreateAPIView: API view to create a new topic.
- ArticlesView: ViewSet for managing Article instances,
  providing full CRUD operations with filtering support.
"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics, status
from rest_framework.response import Response

from articles.filters import ArticleFilter
from articles.models import Article, Topic, TopicFollow
from articles.permissions import OnlyOwnerPermission
from articles.serializers import (
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    TopicSerializer, TopicFollowSerializer,
)


class TopicCreateAPIView(generics.CreateAPIView):
    """
    API view to create a new topic.
    """

    queryset = (
        Topic.objects.all().order_by("name") if hasattr(Topic, "objects") else None
    )
    serializer_class = TopicSerializer


# Create your views here.
class ArticlesView(generics.RetrieveUpdateDestroyAPIView, generics.ListCreateAPIView):
    """
    View for managing Article instances, providing list, create, retrieve, update, and delete operations.
    """

    queryset = Article.objects.all().order_by("-created_at") if hasattr(Article, "objects") else None

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ArticleFilter

    search_fields = ["title", "content", "topics__name", 'summary', ]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ArticleCreateSerializer
        if self.request.method == "PATCH":
            return ArticleDetailSerializer
        return ArticleCreateSerializer

    def get_queryset(self):
        if self.request.method in ["GET", "PATCH", "DELETE"]:
            return self.queryset.filter(status=Article.Status.PUBLISH)
        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        if "pk" in self.kwargs:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [OnlyOwnerPermission]
        self.check_permissions(request)
        instance = self.get_object()
        if instance:
            instance.status = Article.Status.TRASH
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        """
        Custom partial update method to handle PATCH requests.
        """
        self.permission_classes = [OnlyOwnerPermission]
        self.check_permissions(request)
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)


class TopicFollowView(generics.CreateAPIView, generics.DestroyAPIView):
    """
    Handles the API view for creating topic followers.
    """

    queryset = TopicFollow.objects.all() if hasattr(TopicFollow, "objects") else None
    serializer_class = TopicFollowSerializer

    def create(self, request, *args, **kwargs):
        request.data["topic"] = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            topic = serializer.validated_data.get("topic")
            user = request.user
            topic_follow, created = TopicFollow.objects.get_or_create(topic=topic, user=user)

            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            detail_msg = (f"Siz '{topic_follow.topic.name}' mavzusini kuzatyapsiz"
                          if created else
                          f"Siz allaqachon '{topic_follow.topic.name}' mavzusini kuzatyapsiz")
            return Response(status=status_code, data={"detail": detail_msg})

        return Response(data={"detail": "Mavzu berilgan soʻrovga mos kelmaydi."}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        self.permission_classes = [OnlyOwnerPermission]
        self.check_permissions(request)
        instance = TopicFollow.objects.filter(topic_id=kwargs.get("pk"), user=request.user).first()

        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            # return Response(status=st atus.HTTP_404_NOT_FOUND,
            #                 data={"detail": f"Siz '{instance.topic.name}' mavzusini kuzatmaysiz."})
        return Response(status=status.HTTP_404_NOT_FOUND,
                        data={"detail": "Hech qanday mavzu berilgan soʻrovga mos kelmaydi."})
