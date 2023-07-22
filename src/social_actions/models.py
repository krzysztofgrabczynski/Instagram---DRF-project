from django.db import models
from django.contrib.auth import get_user_model

from src.post.models import PostModel


User = get_user_model()


class FollowModel(models.Model):
    """
    Django model for following action.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    user_followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followed"
    )
    followed_user_id = models.PositiveIntegerField(blank=False)

    def __str__(self) -> str:
        return f"Follow(id:{self.id}): {self.user.username}(id:{self.user.id}) -----> {self.user_followed.username}(id:{self.user_followed.id})"

    def __repr__(self) -> str:
        return self.__str__()


class LikeModel(models.Model):
    """
    Django model for thumb up (like) action.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, blank=False)

    def __str__(self) -> str:
        return f"Like(id:{self.id}) of the: {self.user.username}(id:{self.user.id}) under post(id:{self.post.id}) of the: {self.post.user.username}"

    def __repr__(self) -> str:
        return self.__str__()
