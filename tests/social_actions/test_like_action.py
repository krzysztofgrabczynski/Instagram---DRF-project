from tests.user.test_user_update import TestUserUpdateGeneric
from src.social_actions.models import LikeModel
from src.post.models import PostModel


class TestLikeAction(TestUserUpdateGeneric):
    """
    Test module for testing like action.
    Parent class TestUserUpdateGeneric provides setUpTestData and setUp method with creating two users with profiles and tokens.
    """

    def setUp(self) -> None:
        super().setUp()
        self.post = PostModel.objects.create(user=self.user, description="test")

    def test_like_post_by_logged_in_user(self) -> None:
        response = self.client.get(
            f"/post_retrive/{self.post.id}/like/"
        )
        update_post = PostModel.objects.get(id=self.post.id)
        like_obj = LikeModel.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_post.likes, 1)
        self.assertEqual(like_obj.user, self.user)

    def test_unlike_post_by_logged_in_user(self) -> None:
        LikeModel.objects.create(user=self.user, post=self.post)
        self.post.likes += 1
        self.post.save()

        self.assertEqual(LikeModel.objects.count(), 1)
        self.assertEqual(self.post.likes, 1)

        response = self.client.get(
            f"/post_retrive/{self.post.id}/like/"
        )

        update_post = PostModel.objects.get(id=self.post.id)
        like_obj = LikeModel.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_post.likes, 0)
        self.assertEqual(LikeModel.objects.count(), 0)

    def test_like_post_by_logged_out_user(self) -> None:
        self.client.logout()

        response = self.client.get(
            f"/post_retrive/{self.post.id}/like/"
        )

        self.assertEqual(response.status_code, 401)
