from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

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
class ArticleCreateAPIView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateSerializer


    

    def perform_create(self, serializer):
        print(22, self.request.user.username)
        serializer.save(author=self.request.user)


class ArticleDetailAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
