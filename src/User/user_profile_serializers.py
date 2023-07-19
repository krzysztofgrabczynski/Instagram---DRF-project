from rest_framework import serializers
from django.contrib.auth.models import User

from src.user.models import UserProfileModel
from src.post.models import PostModel


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class UserProfileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = [
            "gender",
            "description",
            "posts_amount",
            "followers_amount",
            "following_amount",
        ]


class UserPostDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ["description", "date", "likes"]


class UserProfileSerializer(serializers.Serializer):
    user_data = UserDataSerializer(many=False)
    user_profile_data = UserProfileDataSerializer(many=False)
    user_posts = UserPostDataSerializer(many=True)
