from django.urls import path
from rest_framework.routers import DefaultRouter

from articles import views
from articles.views import ArticlesView

router = DefaultRouter()
router.register(r"articles", ArticlesView, basename="articles")


urlpatterns = [
    path("topic/", view=views.TopicCreateAPIView.as_view()),
]
urlpatterns = router.urls
