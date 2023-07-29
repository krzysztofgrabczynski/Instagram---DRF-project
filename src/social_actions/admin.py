from django.contrib import admin

from src.social_actions.models import FollowModel, LikeModel


admin.site.register(FollowModel)
admin.site.register(LikeModel)
