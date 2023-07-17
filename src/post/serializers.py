from rest_framework import serializers

from src.post.models import PostModel


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for post model.
    Creates a new post by logged in user.
    User field is hidden and default set as logged in user.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PostModel
        fields = "__all__"
        extra_kwargs = {"likes": {"read_only": True}}
