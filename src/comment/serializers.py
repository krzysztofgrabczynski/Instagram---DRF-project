from rest_framework import serializers

from src.comment.models import CommentModel
from src.post.models import PostModel


class CurrentPostDefault:
    """
    Function based on CurrentUserDefault for set HiddenField default as post which is in request.
    If request method is PUT or DELETE, funciton will get post pk from exsiting comment object.
    """

    requires_context = True

    def __call__(self, serializer_field):
        request = serializer_field.context["request"]
        kwargs = request.parser_context["kwargs"]

        if request.method == "PUT" or request.method == "DELETE":
            pk = self._get_post_pk(kwargs)
        else:
            pk = kwargs["pk"]

        default = PostModel.objects.get(pk=pk)
        return default

    def __repr__(self):
        return "%s()" % self.__class__.__name__

    def _get_post_pk(self, kwargs):
        comment = CommentModel.objects.get(pk=kwargs["pk"])
        return comment.post.id


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comment model.
    Creates a new comment by logged in user.
    User field is hidden and default set as logged in user.
    Post field is hidden and default set as post in request using custom function CurrentPostDefault.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.HiddenField(default=CurrentPostDefault())

    class Meta:
        model = CommentModel
        fields = "__all__"
        extra_kwargs = {"likes": {"read_only": True}}
