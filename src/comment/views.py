from rest_framework import mixins, generics, viewsets
from rest_framework.response import Response
from django.http import Http404

from src.comment.models import CommentModel
from src.comment.serializers import CommentSerializer
from src.post.models import PostModel
from src.post.permissions import PostOwnerPermission as CommentOwnerPermission


class CommentCreateView(generics.CreateAPIView):
    """
    Class for creating a comment for specific post object (PostModel).
    """

    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        self._check_post_pk(kwargs["pk"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def _check_post_pk(self, pk: int):
        if not PostModel.objects.filter(pk=pk).exists():
            raise Http404


class CommentUpdateDeleteView(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Class for update/delete a comment for specific post object (PostModel).
    Only owners of the comment object can update or delete the object.
    """

    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentOwnerPermission]
