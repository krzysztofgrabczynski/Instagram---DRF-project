from rest_framework import serializers
from django.contrib.auth.models import User

from src.user.models import UserProfileModel
from src.post.models import PostModel
from src.comment.models import CommentModel


class UserDataSerializer(serializers.ModelSerializer):
    """
    Serializer with username of the user (for UserProfileView).
    """

    class Meta:
        model = User
        fields = ["username"]


class UserProfileDataSerializer(serializers.ModelSerializer):
    """
    Serializer with user profile information of the user (for user UserProfileView).
    """

    class Meta:
        model = UserProfileModel
        fields = [
            "gender",
            "description",
            "posts_amount",
            "followers_amount",
            "following_amount",
        ]


class PostCommentDataSerializer(serializers.ModelSerializer):
    """
    Serializer with all comments udner the specific post (for user UserProfileView).
    """

    class Meta:
        model = CommentModel
        fields = ["user", "text", "date", "likes"]


class UserPostDataSerializer(serializers.ModelSerializer):
    """
    Serializer with all posts of the specific user (for user UserProfileView).
    """

    comments = PostCommentDataSerializer(many=True)

    class Meta:
        model = PostModel
        fields = ["description", "date", "likes", "comments"]


class UserProfileSerializer(serializers.Serializer):
    """
    Serializer for UserProfileView with information about user, user profile and posts that specific user own.
    """

    user_data = UserDataSerializer(many=False)
    user_profile_data = UserProfileDataSerializer(many=False)
    user_posts = UserPostDataSerializer(many=True)
