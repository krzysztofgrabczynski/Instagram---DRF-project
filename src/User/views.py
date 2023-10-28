from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator

from src.user.serializers import (
    UserRegisterSerializer,
    UserAccountUpdateSerializer,
    UserPasswordUpdateSerializer,
    UserProfileSerializer,
    ResetPasswordEmailSerializer,
    ResetPasswordSerializer,
)
from src.user.models import UserProfileModel
from src.user.permissions import UserUpdatePermission
from src.user.tasks import send_reset_password_email_task


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class UserEditAccountView(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountUpdateSerializer
    permission_classes = [UserUpdatePermission]


class UserEditPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPasswordUpdateSerializer
    permission_classes = [UserUpdatePermission]


class UserEditProfileView(generics.UpdateAPIView):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [UserUpdatePermission]


class ResetPassowrdView(viewsets.GenericViewSet):
    """
    View class for reset password functionality.
    It sends an email for provided email address (if user exists in database with that email). Url is created with reset password token and username.
    The token will be deactivated after a successful password reset.
    """

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "send_email":
            return ResetPasswordEmailSerializer
        if self.action == "reset_password":
            return ResetPasswordSerializer

    @action(detail=True, methods=["POST"])
    def send_email(self, request, *args, **kwargs):
        serializer = ResetPasswordEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]

        reset_password_url = self._create_reset_url(request, email)
        send_reset_password_email_task.delay(reset_password_url, email)

        return Response("Email was sent successfully")

    @action(detail=True, methods=["POST"])
    def reset_password(self, request, *args, **kwargs):
        username = kwargs["user"]
        user = User.objects.get(username=username)
        token = kwargs["token"]

        if not default_token_generator.check_token(user, token):
            return Response("Wrong reset password token")

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._perform_set_password(user, serializer)

        return Response("Password reset successfully")

    def _create_reset_url(self, request, email: str) -> str:
        """
        Create reset password url which contains username and token.
        """
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)

        reset_password_url = request.build_absolute_uri(
            reverse("reset_password", kwargs={"user": user, "token": token})
        )

        return reset_password_url

    def _perform_set_password(
        self, user: User, serializer: ResetPasswordSerializer
    ) -> None:
        user.set_password(serializer.data["password"])
        user.save()


send_reset_passoword_email_view = ResetPassowrdView.as_view({"post": "send_email"})
reset_passoword_view = ResetPassowrdView.as_view({"post": "reset_password"})
