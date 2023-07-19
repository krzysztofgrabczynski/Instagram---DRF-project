from django.db import models
from django.contrib.auth.models import User


class PostModel(models.Model):
    """
    Django model for user's posts.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField(default="")
    date = models.DateTimeField(blank=False, auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Post of the: {self.user.username}(id:{self.id})"

    def __repr__(self) -> str:
        return self.__str__()
