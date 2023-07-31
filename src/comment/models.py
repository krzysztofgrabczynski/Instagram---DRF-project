from django.db import models
from django.contrib.auth import get_user_model

from src.post.models import PostModel


User = get_user_model()


class CommentModel(models.Model):
    """
    Django model for comments (using under the posts).
    """

    post = models.ForeignKey(
        PostModel, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(default="")
    date = models.DateTimeField(blank=False, auto_now=True)
    likes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Comment(id:{self.id}) of the: {self.user.username}(id:{self.user.id}) under post(id:{self.post.id}) of the: {self.post.user.username}(id:{self.post.user.id})"

    def __repr__(self) -> str:
        return self.__str__()
