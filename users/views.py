import logging
from secrets import token_urlsafe

from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django_redis import get_redis_connection
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, generics, parsers, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Recommendation
from .errors import ACTIVE_USER_NOT_FOUND_ERROR_MSG
from .serializers import (
    ChangePasswordSerializer,
    ForgotPasswordRequestSerializer,
    ForgotPasswordResponseSerializer,
    ForgotPasswordVerifyRequestSerializer,
    ForgotPasswordVerifyResponseSerializer,
    LoginSerializer,
    RecommendationSerializer,
    ResetPasswordResponseSerializer,
    TokenResponseSerializer,
    UserSerializer,
    UserUpdateSerializer,
    ValidationErrorSerializer,
)
from .services import OTPService, SendEmailService, UserService

logger = logging.getLogger(__name__)

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary="Sign up a new user",
        request=UserSerializer,
        responses={201: UserSerializer, 400: ValidationErrorSerializer},
    )
)
# SignUp qilish uchun class
class SignupView(APIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response(
                {
                    "user": user_data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        summary="Log in a user",
        request=LoginSerializer,
        responses={
            200: TokenResponseSerializer,
            400: ValidationErrorSerializer,
        },
    )
)
# Login qilish uchun class
class LoginView(APIView):
    """
    Log in a user

    """

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            UserService.create_tokens(
                user=user,
                access=str(access),
                refresh=str(refresh),
                is_force_add_to_redis=True,
            )
            return Response(
                {
                    "refresh": str(refresh),
                    "access": access,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Hisob maʼlumotlari yaroqsiz"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


@extend_schema_view(
    get=extend_schema(
        summary="Get user information",
        responses={200: UserSerializer, 400: ValidationErrorSerializer},
    ),
    patch=extend_schema(
        summary="Update user information",
        request=UserUpdateSerializer,
        responses={200: UserUpdateSerializer, 400: ValidationErrorSerializer},
    ),
)
# User malumotlarni olish uchum class
class UsersMe(generics.RetrieveAPIView, generics.UpdateAPIView):
    http_method_names = ["get", "patch"]
    queryset = User.objects.filter(is_active=True)
    permission_classes = (IsAuthenticated,)
    parser_classes = [parsers.MultiPartParser]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UserUpdateSerializer
        return UserSerializer

    def patch(self, request, *args, **kwargs):
        redis_conn = get_redis_connection("default")
        redis_conn.set("test_key", "test_value", ex=3600)
        cached_value = redis_conn.get("test_key")
        return super().partial_update(request, *args, **kwargs)


@extend_schema_view(
    post=extend_schema(
        summary="Log out a user",
        request=None,
        responses={200: ValidationErrorSerializer, 401: ValidationErrorSerializer},
    )
)
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses=None)
    def post(self, request, *args, **kwargs):
        token = UserService.create_tokens(
            request.user,
            access="fake_token",
            refresh="fake_token",
            is_force_add_to_redis=True,
        )
        print(token)
        return Response({"detail": _("Mufaqqiyatli chiqildi.")})


@extend_schema_view(
    put=extend_schema(
        summary="Change user password",
        request=ChangePasswordSerializer,
        responses={200: TokenResponseSerializer, 401: ValidationErrorSerializer},
    )
)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=request.user.username,
            password=serializer.validated_data["old_password"],
        )

        if user is not None:
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            update_session_auth_hash(request, user)
            tokens = UserService.create_tokens(user, is_force_add_to_redis=True)
            return Response(tokens)
        else:
            raise ValidationError(_("Eski parol xato."))


@extend_schema_view(
    post=extend_schema(
        summary="Forgot Password",
        request=ForgotPasswordRequestSerializer,
        responses={
            200: ForgotPasswordResponseSerializer,
            401: ValidationErrorSerializer,
        },
    )
)
class ForgotPasswordView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordRequestSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        users = User.objects.filter(email=email, is_active=True)
        if not users.exists():
            raise exceptions.NotFound(ACTIVE_USER_NOT_FOUND_ERROR_MSG)

        otp_code, otp_secret = OTPService.generate_otp(email=email, expire_in=2 * 60)

        try:
            SendEmailService.send_email(email, otp_code)
            return Response(
                {
                    "email": email,
                    "otp_secret": otp_secret,
                }
            )
        except Exception:
            redis_conn = OTPService.get_redis_conn()
            redis_conn.delete(f"{email}:otp")
            raise ValidationError(_("Emailga xabar yuborishda xatolik yuz berdi"))


@extend_schema_view(
    post=extend_schema(
        summary="Forgot Password Verify",
        request=ForgotPasswordVerifyRequestSerializer,
        responses={
            200: ForgotPasswordVerifyResponseSerializer,
            401: ValidationErrorSerializer,
        },
    )
)
class ForgotPasswordVerifyView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ForgotPasswordVerifyRequestSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        redis_conn = OTPService.get_redis_conn()
        otp_secret = kwargs.get("otp_secret")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_code = serializer.validated_data["otp_code"]
        email = serializer.validated_data["email"]
        users = User.objects.filter(email=email, is_active=True)
        if not users.exists():
            raise exceptions.NotFound(ACTIVE_USER_NOT_FOUND_ERROR_MSG)
        OTPService.check_otp(email, otp_code, otp_secret)
        redis_conn.delete(f"{email}:otp")
        token_hash = make_password(token_urlsafe())
        redis_conn.set(token_hash, email, ex=2 * 60 * 60)
        return Response({"token": token_hash})


@extend_schema_view(
    patch=extend_schema(
        summary="Reset Password",
        request=ResetPasswordResponseSerializer,
        responses={200: TokenResponseSerializer, 401: ValidationErrorSerializer},
    )
)
class ResetPasswordView(generics.UpdateAPIView):
    """
    write documentation
    """

    serializer_class = ResetPasswordResponseSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ["patch"]
    authentication_classes = []

    def patch(self, request, *args, **kwargs):
        redis_conn = OTPService.get_redis_conn()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_hash = serializer.validated_data["token"]
        email = redis_conn.get(token_hash)

        if not email:
            raise ValidationError(_("Token yaroqsiz"))

        users = User.objects.filter(email=email.decode(), is_active=True)
        if not users.exists():
            raise exceptions.NotFound(ACTIVE_USER_NOT_FOUND_ERROR_MSG)

        password = serializer.validated_data["password"]
        user = users.first()
        user.set_password(password)
        user.save()

        update_session_auth_hash(request, user)
        tokens = UserService.create_tokens(user, is_force_add_to_redis=True)
        redis_conn.delete(token_hash)
        return Response(tokens)


class RecommendationView(generics.CreateAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract validated data
        more_recommended = serializer.validated_data.get("more_recommended")
        less_recommended = serializer.validated_data.get("less_recommended")

        # Get or create user's recommendation
        recommendation, _ = Recommendation.objects.get_or_create(user=self.request.user)

        # Manage more_recommended articles
        if more_recommended:
            for article in more_recommended:
                if article in recommendation.less_recommended.all():
                    recommendation.less_recommended.remove(article)
                recommendation.more_recommended.add(article)

        # Manage less_recommended articles
        if less_recommended:
            for article in less_recommended:
                if article in recommendation.more_recommended.all():
                    recommendation.more_recommended.remove(article)
                recommendation.less_recommended.add(article)

        return Response(status=status.HTTP_204_NO_CONTENT)
