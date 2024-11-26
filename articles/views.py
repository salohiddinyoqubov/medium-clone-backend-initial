from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
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

    # def get_queryset(self):
    #     # API'ga so'rov kelganda "get_top_articles" query parametri borligini tekshiramiz.
    #     top_articles = self.request.query_params.get("get_top_articles")
    #     if top_articles:
    #         return Article.objects.order_by("-views_count")[: int(top_articles)]
    #     return super().get_queryset()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
