from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from django.http import Http404

from src.comment.models import CommentModel
from src.comment.serializers import CommentSerializer
from src.post.models import PostModel


class CommentCreateView(generics.CreateAPIView):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        self._check_post_pk(kwargs["pk"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print(args, kwargs)
        return Response(serializer.data)
    
    def _check_post_pk(self, pk: int):
        if not PostModel.objects.filter(pk=pk).exists():
            raise Http404

class CommentUpdateDeleteeView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer

