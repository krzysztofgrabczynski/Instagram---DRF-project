from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from typing import Dict

from src.user.models import UserProfileModel


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    All fields are required.
    Serializer check if the password and password2 are the same and if the username and email are unique.
    """

    email = serializers.EmailField(required=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": True,
                "validators": [validate_password],
            },
        }

    def validate(self, attrs: Dict) -> Dict:
        if not attrs["password"] == attrs["password2"]:
            exc_data = {"password": "Password fields must be the same"}
            raise serializers.ValidationError(exc_data)

        return super().validate(attrs)

    def validate_email(self, email: str) -> str:
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with that email already exists")

        return email


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfileModel model.
    """

    class Meta:
        model = UserProfileModel
        fields = ["gender", "description"]


class UserRegisterSerializer(serializers.Serializer):
    """
    Serializer for registration new user.
    Serializer craetes new user with authentication token and user profile.
    """

    user = UserSerializer(many=False)
    user_profile = UserProfileSerializer(many=False)

    def _create_user_auth_token(self, user: User) -> Token:
        token = Token.objects.create(user=user)

        return token

    def _create_user_profile(
        self, user: User, validated_data: Dict
    ) -> UserProfileModel:
        user_profile = UserProfileModel.objects.create(
            user=user,
            gender=validated_data["gender"],
            description=validated_data["description"],
        )

        return user_profile

    def create(self, validated_data: Dict) -> User:
        validated_user_data = validated_data["user"]
        validated_user_profile_data = validated_data["user_profile"]

        user = User.objects.create_user(
            username=validated_user_data["username"],
            email=validated_user_data["email"],
            password=validated_user_data["password"],
        )

        self._create_user_auth_token(user)
        self._create_user_profile(user, validated_user_profile_data)

        return validated_data


class UserAccountUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for update account data for specific user. Could change username and email.
    """

    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]

    def validate_email(self, email: str) -> str:
        if (
            User.objects.filter(email=email).exists()
            and not self.instance.email == email
        ):
            raise serializers.ValidationError("User with that email already exists")

        return email


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for change password of the specific user. Old password must be correct and new passwords have to be validated.
    """

    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["old_password", "password", "password2"]

    def validate(self, attrs: Dict) -> Dict:
        if not attrs["password"] == attrs["password2"]:
            exc_data = {"password": "Password fields must be the same"}
            raise serializers.ValidationError(exc_data)

        return super().validate(attrs)

    def validate_old_password(self, old_password: str) -> str:
        if old_password:
            if not self.instance.check_password(old_password):
                raise serializers.ValidationError("Password incorrect")

        return old_password

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class ResetPasswordEmailSerializer(serializers.Serializer):
    """
    Serializer for provide email for send message with reset password url.
    """

    email = serializers.EmailField(required=True)

    def validate_email(self, email: str) -> str:
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with that email does not exists")

        return email


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for insert a new password using reset password url.
    """

    password = serializers.CharField(required=True, validators=[validate_password])
    password2 = serializers.CharField(required=True)

    def validate(self, attrs: Dict) -> Dict:
        if not attrs["password"] == attrs["password2"]:
            exc_data = {"password": "Password fields must be the same"}
            raise serializers.ValidationError(exc_data)

        return super().validate(attrs)
