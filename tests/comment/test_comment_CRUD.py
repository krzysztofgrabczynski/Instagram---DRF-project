from src.post.models import PostModel
from src.comment.models import CommentModel
from tests.user.test_user_update import TestUserUpdateGeneric as GenericTestCase


class TestCreateComment(GenericTestCase):
    """
    Test module for testing creating a new comment object.
    Inherits from TestUserUpdateGeneric which creates two users with tokens and logging one of them.
    """

    def setUp(self) -> None:
        super().setUp()
        self.post = PostModel.objects.create(
            user=self.user, description="test_description"
        )

    def test_create_comment_with_valid_data(self) -> None:
        response = self.client.post(
            f"/create_comment/{self.post.id}/", {"text": "test_description"}
        )
        comment = CommentModel.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CommentModel.objects.count(), 1)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.text, "test_description")

    def test_create_comment_with_invalid_post_pk(self) -> None:
        response = self.client.post(f"/create_comment/{-1}/")
        comment = CommentModel.objects.first()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(CommentModel.objects.count(), 0)


class TestUpdateDeleteComment(GenericTestCase):
    """
    Test module for testing update/delete comment object.
    Inherits from TestUserUpdateGeneric which creates two users with tokens and logging one of them.
    """

    def setUp(self) -> None:
        super().setUp()
        self.post = PostModel.objects.create(
            user=self.user, description="test_description"
        )
        self.comment = CommentModel.objects.create(
            post=self.post, user=self.user, text="test_text"
        )

    def test_update_comment_with_valid_data(self) -> None:
        response = self.client.put(
            f"/comment/{self.comment.id}/", {"text": "test_text_update"}
        )
        comment = CommentModel.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CommentModel.objects.count(), 1)
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.text, "test_text_update")

    def test_update_comment_with_invalid_user(self) -> None:
        self.client.logout()
        self.client.login(username=self.user2.username, password="test_password")
        self.client.credentials(HTTP_AUTHORIZATION=self.token2)

        response = self.client.put(
            f"/comment/{self.comment.id}/", {"text": "test_text_update"}
        )

        self.assertEqual(response.status_code, 403)

    def test_delete_comment_with_valid_data(self) -> None:
        self.assertEqual(CommentModel.objects.count(), 1)

        self.client.delete(f"/comment/{self.comment.id}/")

        self.assertEqual(CommentModel.objects.count(), 0)

    def test_delete_comment_with_invalid_user(self) -> None:
        self.client.logout()
        self.client.login(username=self.user2.username, password="test_password")
        self.client.credentials(HTTP_AUTHORIZATION=self.token2)

        response = self.client.delete(f"/comment/{self.comment.id}/")

        self.assertEqual(response.status_code, 403)
