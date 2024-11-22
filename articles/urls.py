from django.urls import path

from articles import views

urlpatterns = [
    path("topic/", view=views.TopicCreateAPIView.as_view()),
    path("articles/", view=views.ArticleCreateAPIView.as_view()),
    path("articles/<int:pk>/", view=views.ArticleDetailAPIView.as_view()),
]
