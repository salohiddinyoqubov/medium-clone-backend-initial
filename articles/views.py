from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
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
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


# Create your views here.
class ArticlesView(viewsets.ModelViewSet):

    queryset = Article.objects.all()
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
        if self.action == "list":
            queryset = Article.objects.filter(status="publish")
            return queryset
        if self.action == "retrieve":
            queryset = Article.objects.filter(status="publish")
            return queryset


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
        return Response(status=status.HTTP_403_FORBIDDEN, data={"detail": "Not authorized."})