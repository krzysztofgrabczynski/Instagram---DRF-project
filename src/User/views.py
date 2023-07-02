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
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        username = request.data.get("username", instance.username)
        email = request.data.get("email", instance.email)
        
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class UserEditProfileView(generics.UpdateAPIView):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer


