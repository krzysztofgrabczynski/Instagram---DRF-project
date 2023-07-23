from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from src.social_actions.models import LikeModel


class LikeActionMixin:
    """
    Mixin for creating new LikeModel object or delete existing.
    Working with viewsets.
    It is used with models that have 'likes' attribute.
    You need to set 'like_action_queryset' as queryset of the model that will user like action.
    In addition you need to set 'new_like_obj_lookup_field' which will be used to create new like object (it is for relationship fields in models).
    """
    like_action_queryset = None
    like_action_lookup_field = "pk"
    new_like_obj_lookup_field = None

    def get_like_action_queryset(self):
        assert self.queryset is not None, (
            f"'{self.__class__.__name__}' should either include a `queryset` attribute, "
            "or override the `get_like_action_queryset()` method."
        )

        queryset = self.like_action_queryset

        assert hasattr(queryset.model, "likes"), (
            f'Expected view {self.__class__.__name__} should include a model with "likes" attribute. '
            "Check the `.like_action_queryset` field."
        )

        if isinstance(queryset, QuerySet):
            queryset = queryset.all()

        return queryset

    def get_like_action_object(self):
        queryset = self.get_like_action_queryset()

        assert self.like_action_lookup_field in self.kwargs, (
            f"Expected view {self.__class__.__name__} to be called with a URL keyword argument"
            f"named '{self.like_action_lookup_field}'. Fix your URL conf, or set the `.like_action_lookup_field` "
            "attribute on the view correctly."
        )

        pk = self.kwargs[self.like_action_lookup_field]
        obj = get_object_or_404(queryset, pk=pk)

        return obj

    @action(detail=True, methods=["GET"])
    def like(self, request, *args, **kwargs):
        obj = self.get_like_action_object()

        assert self.new_like_obj_lookup_field is not None, (
            f"Expected view {self.__class__.__name__} should include a not None `.new_like_obj_lookup_field` value. "
            "Fix your URL conf, or set the `.new_like_obj_lookup_field` "
            "attribute on the view correctly."
        )

        for like in obj.likemodel_set.all():
            if like in request.user.likemodel_set.all():
                self._delete_like(like, obj)

                return Response("unlike")

        self._create_like(request.user, obj)

        return Response("like")

    def _delete_like(self, like, obj):
        like.delete()
        obj.likes -= 1
        obj.save()

    def _create_like(self, user, obj):
        data = {"user": user, f"{self.new_like_obj_lookup_field}": obj}
        new_like = LikeModel.objects.create(**data)
        new_like.save()
        obj.likes += 1
        obj.save()
