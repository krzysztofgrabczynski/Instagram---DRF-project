from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from typing import Dict

from src.user.models import UserProfileModel


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registration new user.
    All fields are required. Username and email must be unique. Password and password2 must be the same.
    This serializer craetes authentication token for user and user profile.
    """

    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2", "gender", "description"]
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
            "email": {"required": True},
        }

    def validate(self, attrs: Dict) -> Dict:
        if attrs["password"] is not attrs["password2"]:
            exc_data = {"password": "Password fields must be the same"}
            raise serializers.ValidationError(exc_data)

        return super().validate(attrs)

    def validate_email(self, email: str) -> str:
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with that email already exists")

        return email

    def _create_user_auth_token(self, user: User) -> Token:
        token = Token.objects.create(user=user)

        return token

    def _create_user_profile(self, user: User, validated_data: Dict) -> None:
        UserProfileModel.objects.craete(
            user=user,
            gender=validated_data["gender"],
            description=validated_data["description"],
        )

    def craete(self, validated_data: Dict) -> User:
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        self._create_user_auth_token(user)
        self._create_user_profile(user, validated_data)

        return user
