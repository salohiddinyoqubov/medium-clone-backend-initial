from django.urls import path
from rest_framework.routers import DefaultRouter

from articles import views
from articles.views import ArticleView

router = DefaultRouter()
router.register(r"articles", ArticleView, basename="articles")


urlpatterns = [
    path("topic/", view=views.TopicCreateAPIView.as_view()),
]
urlpatterns = router.urls
