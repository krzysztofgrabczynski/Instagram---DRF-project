from rest_framework import viewsets, mixins

from src.post.serializers import PostSerializer
from src.post.models import PostModel


class PostCreateUpdateDeleteView(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    View for create, update and delete specific post.
    It uses the GenericViewSet for router functionality.
    """
    queryset = PostModel.objects.all()
    serializer_class = PostSerializer
    
