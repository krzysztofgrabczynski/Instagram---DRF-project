from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import pytest

from src.user.models import UserProfileModel


class TestUserUpdateGeneric(TestCase):
    """
    Generic class for user update tests with setUp and setUpTestData method.
    Creates two users and logged in one of them for testing.
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

        user_data_2 = {
            "username": "test_user_2",
            "email": "test_2@email.com",
            "password": "test_password",
        }
        user2 = User.objects.create_user(**user_data_2)
        UserProfileModel.objects.create(user=user2, description="test_description")
        Token.objects.create(user=user2)

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.get(username="test_user")
        self.user_profile = UserProfileModel.objects.get(user=self.user)
        self.token = "Token " + str(self.user.auth_token)
        self.client.login(username="test_user", password="test_password")
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        self.user2 = User.objects.get(username="test_user_2")
        self.user_profile2 = UserProfileModel.objects.get(user=self.user2)
        self.token2 = "Token " + str(self.user2.auth_token)


class TestUserAccountUpdate(TestUserUpdateGeneric):
    """
    A class for testing user account update functionality.
    """

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

    def test_logged_out_user(self):
        self.client.logout()
        response = self.client.put(
            f"/edit_account/{self.user.id}/",
            {"username": "test_user_update", "email": "test_update@email.com"},
        )

        content = str(response.content.decode())
        excpected_msg = """{"detail":"Authentication credentials were not provided."}"""

        self.assertEqual(response.status_code, 401)
        self.assertEqual(content, excpected_msg)

    def test_user_account_update_with_wrong_user(self):
        response = self.client.put(
            f"/edit_account/{self.user2.id}/",
            {"username": "test_user_update", "email": "test_update@email.com"},
        )

        content = str(response.content.decode())
        excpected_msg = (
            """{"detail":"You do not have permission to perform this action."}"""
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(content, excpected_msg)


class TestUserPasswordUpdate(TestUserUpdateGeneric):
    """
    A class for testing user password update functionality.
    """

    def test_user_password_update_with_valid_data(self):
        response = self.client.put(
            f"/edit_password/{self.user.id}/",
            {
                "old_password": "test_password",
                "password": "test_password_2",
                "password2": "test_password_2",
            },
        )

        update_user = User.objects.get(id=self.user.id)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(update_user.check_password("test_password_2"))

    def test_user_password_update_with_invalid_old_password(self):
        response = self.client.put(
            f"/edit_password/{self.user.id}/",
            {
                "old_password": "incorrect",
                "password": "test_password_2",
                "password2": "test_password_2",
            },
        )

        content = str(response.content.decode())
        excpected_msg = """{"old_password":["Password incorrect"]}"""
        update_user = User.objects.get(id=self.user.id)

        self.assertEqual(response.status_code, 400)
        self.assertTrue(update_user.check_password("test_password"))
        self.assertEqual(content, excpected_msg)

    def test_user_password_update_with_not_same_password_and_password2(self):
        response = self.client.put(
            f"/edit_password/{self.user.id}/",
            {
                "old_password": "test_password",
                "password": "test_password_2",
                "password2": "not_same_password",
            },
        )

        content = str(response.content.decode())
        excpected_msg = """{"password":["Password fields must be the same"]}"""
        update_user = User.objects.get(id=self.user.id)

        self.assertEqual(response.status_code, 400)
        self.assertTrue(update_user.check_password("test_password"))
        self.assertEqual(content, excpected_msg)

    def test_logged_out_user(self):
        self.client.logout()
        response = self.client.put(
            f"/edit_password/{self.user.id}/",
            {
                "old_password": "test_password",
                "password": "test_password_2",
                "password2": "not_same_password",
            },
        )

        content = str(response.content.decode())
        excpected_msg = """{"detail":"Authentication credentials were not provided."}"""

        self.assertEqual(response.status_code, 401)
        self.assertEqual(content, excpected_msg)

    def test_user_account_update_with_wrong_user(self):
        response = self.client.put(
            f"/edit_password/{self.user2.id}/",
            {
                "old_password": "test_password",
                "password": "test_password_2",
                "password2": "not_same_password",
            },
        )

        content = str(response.content.decode())
        excpected_msg = (
            """{"detail":"You do not have permission to perform this action."}"""
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(content, excpected_msg)


class TestUserProfileUpdate(TestUserUpdateGeneric):
    """
    A class for testing user profile update functionality.
    """

    def test_user_profile_update_with_valid_data(self):
        response = self.client.put(
            f"/edit_profile/{self.user_profile.id}/",
            {
                "gender": 1,
                "description": "update_description",
            },
        )

        update_user_profile = UserProfileModel.objects.get(id=self.user_profile.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_user_profile.gender, 1)
        self.assertEqual(update_user_profile.description, "update_description")

    def test_logged_out_user(self):
        self.client.logout()
        response = self.client.put(
            f"/edit_profile/{self.user_profile.id}/",
            {
                "gender": 1,
                "description": "update_description",
            },
        )

        content = str(response.content.decode())
        excpected_msg = """{"detail":"Authentication credentials were not provided."}"""

        self.assertEqual(response.status_code, 401)
        self.assertEqual(content, excpected_msg)

    def test_user_account_update_with_wrong_user(self):
        response = self.client.put(
            f"/edit_profile/{self.user_profile2.id}/",
            {
                "gender": 1,
                "description": "update_description",
            },
        )

        content = str(response.content.decode())
        excpected_msg = (
            """{"detail":"You do not have permission to perform this action."}"""
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(content, excpected_msg)
