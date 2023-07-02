from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response

from src.user.serializers import UserRegisterSerializer, UserSerializer, UserProfileSerializer
from src.user.models import UserProfileModel


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


class UserEditAccountView(generics.UpdateAPIView):
    pass


class UserEditProfileView(generics.UpdateAPIView):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer


