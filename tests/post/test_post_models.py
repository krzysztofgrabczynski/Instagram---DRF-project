from django.test import TestCase
from django.contrib.auth.models import User

from src.post.models import PostModel


class TestPostModel(TestCase):
    """
    Test module for testing PostModel.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(username="test1", password="test")
        PostModel.objects.create(user=user, description="test")

    def test_str_method(self) -> None:
        """
        Testing __str__() and __repr__() methods.
        When calling CommentwModel object, should return a string: "Post of the: <user.username>(id:<post.id>)"
        """
        user = User.objects.first()
        post = PostModel.objects.first()
        expected = f"Post of the: {user.username}(id:{post.id})"

        self.assertEqual(expected, str(expected))
