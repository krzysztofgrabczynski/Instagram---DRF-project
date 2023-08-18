from django.test import TestCase
from django.contrib.auth.models import User

from src.social_actions.models import FollowModel, LikeModel
from src.post.models import PostModel


class TestFollowModel(TestCase):
    """
    Test module for testing FollowModel.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        use1 = User.objects.create_user(username="test1", password="test")
        user2 = User.objects.create_user(username="test2", password="test")

        FollowModel.objects.create(user=use1, user_followed=user2)

    def test_str_method(self) -> None:
        """
        Testing __str__() and __repr__() methods.
        When calling FollowModel object, should return a string: "Follow(id:(<follow obj id>)): (<user1 username>)(id:(<user1 id>)) -----> (<user2 username>)(id:(<user2 id>))"
        """
        user1 = User.objects.get(username="test1")
        user2 = User.objects.get(username="test2")
        follow_obj = FollowModel.objects.first()
        expected = f"Follow(id:{follow_obj.id}): {user1.username}(id:{user1.id}) -----> {user2.username}(id:{user2.id})"

        self.assertEqual(expected, str(follow_obj))


class TestLikeModel(TestCase):
    """
    Test module for testing LikeModel.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(username="test", password="test")

        post = PostModel.objects.create(user=user, description="test description")
        LikeModel.objects.create(user=user, post=post)

    def test_str_method(self) -> None:
        """
        Testing __str__() and __repr__() methods.
        When calling FollowModel object, should return a string: "Like(id:(<like obj id>)) of the: (<user username>)(id:(<user id>)) under post(id:(<post id>)) of the: (<post user username>)"
        """
        user = User.objects.get(username="test")
        post = PostModel.objects.first()
        like_obj = LikeModel.objects.first()
        expected = f"Like(id:{like_obj.id}) of the: {user.username}(id:{user.id}) under post(id:{post.id}) of the: {post.user.username}"

        self.assertEqual(expected, str(like_obj))
