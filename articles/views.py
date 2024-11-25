from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from articles.models import Article, Topic
from articles.serializers import (
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    TopicSerializer,
)


class TopicCreateAPIView(generics.CreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


# Create your views here.
class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ArticleCreateSerializer
        if self.action == "retrieve":
            return ArticleDetailSerializer
        return ArticleCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        print(22, self.request.user.username)
        serializer.save(author=self.request.user)
