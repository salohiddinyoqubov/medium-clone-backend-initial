"""
This module defines the URL routing for the articles' application.
It sets up paths for views related to articles and topics, 
utilizing Django Rest Framework's routing mechanism.
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from articles import views
from articles.views import ArticlesView, TopicFollowView

urlpatterns = [
    path("articles/<int:pk>/", ArticlesView.as_view(), name="articles_update_destroy"),
    path("articles/", ArticlesView.as_view(), name="articles_get_create"),

    path("articles/topics/<int:pk>/follow/", view=TopicFollowView.as_view()),
    path("articles/topic/", view=views.TopicCreateAPIView.as_view()),
]
