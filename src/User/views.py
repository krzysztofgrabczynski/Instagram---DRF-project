from django.contrib.auth.models import User
from rest_framework import generics

from src.user.serializers import (
    UserRegisterSerializer,
    UserAccountUpdateSerializer,
    UserPasswordUpdateSerializer,
    UserProfileSerializer,
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
    # permission_classes = [UserUpdatePermission]


class UserEditProfileView(generics.UpdateAPIView):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [UserUpdatePermission]
