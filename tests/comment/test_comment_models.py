from django.test import TestCase
from django.contrib.auth.models import User

from src.post.models import PostModel
from src.comment.models import CommentModel


class TestCommentModel(TestCase):
    """
    Test module for testing CommentModel.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        user1 = User.objects.create_user(username="test1", password="test")
        post = PostModel.objects.create(user=user1, description="test")
        CommentModel.objects.create(post=post, user=user1, text="test")

    def test_str_method(self) -> None:
        """
        Testing __str__() and __repr__() methods.
        When calling CommentwModel object, should return a string: "Comment(id:(<comment id>)) of the: (<user username>)(id:(<user id>)) under post(id:(<post id>)) of the: (<post user username>)(id:(<post user id>))"
        """
        comment_obj = CommentModel.objects.first()
        post = comment_obj.post
        user = comment_obj.user
        expected = f"Comment(id:{comment_obj.id}) of the: {user.username}(id:{user.id}) under post(id:{post.id}) of the: {post.user.username}(id:{post.user.id})"

        self.assertEqual(expected, str(comment_obj))
