from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from src.user.serializers import (
    UserRegisterSerializer,
    UserAccountUpdateSerializer,
    UserPasswordUpdateSerializer,
    UserProfileSerializer,
    ResetPasswordEmailSerializer,
)
from src.user.models import UserProfileModel
from src.user.permissions import UserUpdatePermission


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
    def _custom_send_email(self, reset_password_url, email):
        subject = "Reset password"
        message = f"Click here to reset your password: {reset_password_url}"
        from_email = ...
        recipient_list = [email]
        print(f"Send email to {recipient_list}")
        # send_mail(subject, message, from_email, recipient_list)

    @action(detail=True, methods=["POST"])
    def send_email(self, request, *args, **kwargs):
        email = kwargs["email"]
        self.token = "example_token"
        reset_password_url = request.build_absolute_uri(
            reverse("reset_password", kwargs={"token": self.token})
        )

        self._custom_send_email(reset_password_url, email)

        return Response(reset_password_url)

    @action(detail=True, methods=["POST"])
    def reset_password(self, request, *args, **kwargs):
        post_token = kwargs.pop("token", None)
        if not post_token == self.token:
            return Response("Wrong reset password token")

        return Response("not implemented")


send_reset_passoword_email_view = ResetPassowrdView.as_view({"post": "send_email"})
reset_passoword_view = ResetPassowrdView.as_view({"post": "reset_password"})
