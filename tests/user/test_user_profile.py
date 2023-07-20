from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from tests.user.test_user_registration import TestGenericUserRegistration as func
from src.user.models import UserProfileModel
from src.post.models import PostModel


class TestUserProfile(TestCase):
    """
    Class for user profile tests.
    It creates user (setUpTestData method) and logged in (setUp method) for testing.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        user_data = {
            "username": "test_user",
            "email": "test@email.com",
            "password": "test_password",
        }
        user = User.objects.create_user(**user_data)
        UserProfileModel.objects.create(user=user, description="test_description")
        Token.objects.create(user=user)

        PostModel.objects.create(user=user, description="test_post_description")

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.get(username="test_user")
        self.user_profile = UserProfileModel.objects.get(user=self.user)
        self.token = "Token " + str(self.user.auth_token)
        self.client.login(username="test_user", password="test_password")
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_user_profile_check_data(self):
        response = self.client.get(
            f"/user_profile/{self.user.id}/"
        )

        content = func.byte_content_to_dict(response.content)
        user_content = content["user_data"]
        profile_content = content["user_profile_data"]
        post_content = content["user_posts"]

        print(content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(user_content["username"], "test_user")
        self.assertEqual(profile_content["description"], "test_description")
        self.assertEqual(post_content[0]["description"], "test_post_description")
