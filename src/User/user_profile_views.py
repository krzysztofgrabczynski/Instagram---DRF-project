from rest_framework import generics
from rest_framework.response import Response

from src.user.user_profile_serializers import UserProfileSerializer
from src.user.models import UserProfileModel


class UserProfileView(generics.RetrieveAPIView):
    """
    APIView for user profile.
    """

    queryset = UserProfileModel.objects.all()
    serializer_class = UserProfileSerializer

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