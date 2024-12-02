from django.urls import path
from rest_framework.routers import DefaultRouter
from setuptools.extern import names

from users import views
#
# router = DefaultRouter()
# router.register(r"recommend", views.RecommendationView, basename="recommend")

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("me/", views.UsersMe.as_view(), name="users-me"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password/change/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path(
        "password/forgot/", views.ForgotPasswordView.as_view(), name="forgot-password"
    ),
    path(
        "password/forgot/verify/<str:otp_secret>/",
        views.ForgotPasswordVerifyView.as_view(),
        name="forgot-verify",
    ),
    path("password/reset/", views.ResetPasswordView.as_view(), name="reset-password"),
    path("recommend/", views.RecommendationView.as_view(), name='user_recommend')
]
