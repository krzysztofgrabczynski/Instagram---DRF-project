from rest_framework import mixins, viewsets
from rest_framework.response import Response

from src.user.user_profile_serializers import UserProfileSerializer
from src.user.models import UserProfileModel
from src.social_actions.mixins import FollowActionMixin


class UserProfileView(
    FollowActionMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    APIView for user profile.
    """

    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer
    user_profile_queryset = UserProfileModel.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Updating retrieve method by creating 'neasted_instance' for nested serializer UserProfileSerializer.
        """
        instance = self.get_object()
        nested_instance = self._create_nested_instance(instance)
        serializer = self.get_serializer(nested_instance)
        return Response(serializer.data)

    def _create_nested_instance(self, instance: UserProfileModel) -> dict:
        user = instance.user
        posts = instance.user.posts.all().order_by("-date")
        nested_instance = {
            "user_data": user,
            "user_profile_data": instance,
            "user_posts": posts,
        }

        return nested_instance
