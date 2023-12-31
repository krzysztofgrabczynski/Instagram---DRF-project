from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from typing import Any

from src.social_actions.models import LikeModel
from src.social_actions.models import FollowModel
from src.user.models import UserProfileModel


class LikeActionMixin:
    """
    Mixin for creating new LikeModel object or delete existing.
    Working with viewsets.
    It is used with models that have 'likes' attribute.
    You need to set 'like_action_queryset' as queryset of the model that will use like action.
    In addition you need to set 'new_like_obj_lookup_field' which will be used to create new like object (it is for relationship fields in models).
    """

    like_action_queryset = None
    like_action_lookup_field = "pk"
    new_like_obj_lookup_field = None

    def get_like_action_queryset(self):
        queryset = self.like_action_queryset

        assert self.queryset is not None, (
            f"'{self.__class__.__name__}' should either include a `queryset` attribute, "
            "or override the `get_like_action_queryset()` method."
        )

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

    def _delete_like(self, like: LikeModel, obj: Any) -> None:
        like.delete()
        obj.likes -= 1
        obj.save()

    def _create_like(self, user: User, obj: Any) -> None:
        data = {"user": user, f"{self.new_like_obj_lookup_field}": obj}
        new_like = LikeModel.objects.create(**data)
        new_like.save()
        obj.likes += 1
        obj.save()


class FollowActionMixin:
    """
    Mixin for creating new FollowModel object or delete existing.
    Follow action will delete existing FollowModel object if exists or create new FollowModel object or none of these if logged user is owner of the user profile.
    Working with viewsets.
    You need to set 'user_profile_queryset' as queryset of the model that will use follow action.
    It increases follow amounts on users profiles or decreases (depends if the follow or unfollow action)
    """

    user_profile_queryset = None
    user_profile_lookup_field = "pk"

    def get_user_profile_object(self):
        queryset = self.user_profile_queryset

        assert self.user_profile_lookup_field in self.kwargs, (
            f"Expected view {self.__class__.__name__} to be called with a URL keyword argument"
            f"named '{self.user_profile_lookup_field}'. Fix your URL conf, or set the `.user_profile_lookup_field` "
            "attribute on the view correctly."
        )

        pk = self.kwargs[self.user_profile_lookup_field]
        obj = get_object_or_404(queryset, pk=pk)

        return obj

    @action(detail=True, methods=["GET"])
    def follow_action(self, request, *args, **kwargs):
        profile = self.get_user_profile_object()
        if request.user == profile.user:
            return Response("Logged user profile")

        follow_obj = self._check_if_following(request.user, profile)
        if follow_obj:
            self._unfollow(request.user, profile, follow_obj)
            return Response("Unfollow")

        self._create_follow(request.user, profile)
        return Response("Follow")

    def _check_if_following(self, user: User, profile: UserProfileModel) -> bool:
        follow_obj = user.follower.filter(user_followed=profile.user)
        return follow_obj if follow_obj else None

    def _create_follow(self, user: User, profile: UserProfileModel) -> None:
        new_follow = FollowModel.objects.create(user=user, user_followed=profile.user)
        new_follow.save()

        user.userprofilemodel.following_amount += 1
        user.userprofilemodel.save()
        profile.followers_amount += 1
        profile.save()

    def _unfollow(
        self, user: User, profile: UserProfileModel, follow: FollowModel
    ) -> None:
        follow.delete()

        user.userprofilemodel.following_amount -= 1
        user.userprofilemodel.save()
        profile.followers_amount -= 1
        profile.save()
