from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response

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
    permission_classes = [UserUpdatePermission]

    def update(self, request, *args, **kwargs):
        """
        Edit of the update method -> added "pk" into serializer instance to use the logged user object.
        """
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, user_pk=kwargs["pk"]
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class UserEditProfileView(generics.UpdateAPIView):
    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [UserUpdatePermission]
