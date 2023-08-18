from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from src.post.serializers import PostSerializer
from src.post.models import PostModel
from src.post.permissions import PostOwnerPermission
from src.social_actions.mixins import LikeActionMixin


class PostCreateUpdateDeleteView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    View for create, update and delete specific post.
    It uses the GenericViewSet for router functionality.
    Post obj can be update/delete only by the owner of that obj.
    """

    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostOwnerPermission]


class PostRetriveView(
    LikeActionMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    View for retrive PostModel objects.
    It uses LikeActionMixin for like action functionality.
    User has to be logged in to retrieve obj.
    """

    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    like_action_queryset = PostModel.objects.all()
    new_like_obj_lookup_field = "post"
