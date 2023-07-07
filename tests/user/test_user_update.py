from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from src.user.models import UserProfileModel
from tests.user.test_user_registration import UserRegistrationsTestCase as func


class TestUserUpdateGeneric(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user_data = {
            "username": "test_user",
            "email": "test@email.com",
            "password": "test_password",
        }
        user = User.objects.create_user(**user_data)
        UserProfileModel.objects.create(user=user, description="test_description")

        user_data_2 = {
            "username": "test_user_2",
            "email": "test_2@email.com",
            "password": "test_password",
        }
        user = User.objects.create_user(**user_data_2)

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.get(username="test_user")
        self.user_profile = UserProfileModel.objects.get(user=self.user)


class TestUserAccountUpdate(TestUserUpdateGeneric):
    def test_user_account_update_with_valid_data(self):
        response = self.client.put(
            f"/edit_account/{self.user.id}/",
            {"username": "test_user_update", "email": "test_update@email.com"},
        )
        update_user = User.objects.get(id=self.user.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_user.username, "test_user_update")
        self.assertEqual(update_user.email, "test_update@email.com")

    def test_user_account_update_with_exists_username(self):
        response = self.client.put(
            f"/edit_account/{self.user.id}/",
            {"username": "test_user_2", "email": "test_update@email.com"},
        )

        content = str(response.content.decode())
        excpected_msg = """{"username":["A user with that username already exists."]}"""

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, excpected_msg)

    def test_user_account_update_with_exists_email(self):
        response = self.client.put(
            f"/edit_account/{self.user.id}/",
            {"username": "test_user_update", "email": "test_2@email.com"},
        )

        content = str(response.content.decode())
        excpected_msg = """{"email":["User with that email already exists"]}"""

        self.assertEqual(response.status_code, 400)
        self.assertEqual(content, excpected_msg)
