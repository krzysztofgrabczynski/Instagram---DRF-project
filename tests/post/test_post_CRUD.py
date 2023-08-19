from src.post.models import PostModel
from tests.user.test_user_update import TestUserUpdateGeneric as GenericTestCase


class TestCreatePost(GenericTestCase):
    """
    Test module for testing create a new post object.
    Inherits from TestUserUpdateGeneric which creates two users with tokens and logging one of them.
    """

    def test_create_post_with_valid_data(self) -> None:
        response = self.client.post(
            f"/post/", {"description": "test_description"}
        )
        post = PostModel.objects.first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(PostModel.objects.count(), 1)
        self.assertEqual(post.user, self.user)
        self.assertEqual(post.description, "test_description")

    def test_create_post_with_logged_out_user(self) -> None:
        self.client.logout()

        response = self.client.post(
            f"/post/", {"description": "test_description"}
        )

        self.assertEqual(response.status_code, 401)

class TestUpdateDeletePost(GenericTestCase):
    """
    Test module for testing update/delete post object.
    Inherits from TestUserUpdateGeneric which creates two users with tokens and logging one of them.
    """

    def setUp(self) -> None:
        super().setUp()
        self.post = PostModel.objects.create(
            user=self.user, description="test_description"
        )

    def _change_logged_user(self, user: str, password: str, token: str) -> None:
        self.client.logout()
        self.client.login(username=user, password=password)
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_update_post_with_valid_user(self) -> None:
        self.assertEqual(self.post.description, "test_description")

        response = self.client.put(
            f"/post/{self.post.id}/", {"description": "update_descrioption"}
        )
        
        update_post = PostModel.objects.get(id=self.post.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_post.description, "update_descrioption")

    def test_update_post_with_invalid_user(self) -> None:
        self._change_logged_user(self.user2, self.user2.password, self.token2)

        response = self.client.put(
            f"/post/{self.post.id}/", {"description": "update_descrioption"}
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_post_with_valid_user(self) -> None:
        self.assertEqual(PostModel.objects.count(), 1)

        response = self.client.delete(
            f"/post/{self.post.id}/", {"description": "delete_descrioption"}
        )
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(PostModel.objects.count(), 0)

    def test_delete_post_with_invalid_user(self) -> None:
        self._change_logged_user(self.user2, self.user2.password, self.token2)

        response = self.client.delete(
            f"/post/{self.post.id}/", {"description": "delete_descrioption"}
        )

        self.assertEqual(response.status_code, 403)
