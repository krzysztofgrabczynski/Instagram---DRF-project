from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User

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
        user = instance.user
        nested_instance = {
            "user_data": user,
            "user_profile_data": instance,
            "user_posts": user.posts,
        }
        serializer = self.get_serializer(nested_instance)
        return Response(serializer.data)
