from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework import generics, views
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


class ResetPassowrdView(views.APIView):
    def get(self, request, *args, **kwargs):
        reset_password_url = request.build_absolute_uri(reverse("reset_password", kwargs={"token": self.token}))

        subject = 'Reset password'
        message = f"Click here to reset your password: {reset_password_url}"
        from_email = ...
        recipient_list = [...]
        send_mail(subject, message, from_email, recipient_list)

        return Response(reset_password_url)
    
    def post(self, request, *args, **kwargs):
        post_token = kwargs.pop("token", None)
        print(post_token)
        