from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import json


class UserRegistrationsTestCase(TestCase):
    """
    Generic class for user registration tests with setUp method.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        user_data = {
            "username": "test_username",
            "email": "test_email@test.com",
            "password": "testpassword123!",
            "password2": "testpassword123!",
        }
        user_pofile_data = {"gender": 1, "description": "test_description"}
        self.data = json.dumps(dict(user=user_data, user_profile=user_pofile_data))


class TestGenericUserRegistration(UserRegistrationsTestCase):
    """
    Generic test cases for user registration.
    """

    def test_user_registration_with_valid_data(self):
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(
            "/sign_up/", self.data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)


class TestUserRegistrationPositiveResponseContent(UserRegistrationsTestCase):
    """
    Test cases for checking response content for valid post data.
    """

    def setUp(self) -> None:
        super().setUp()
        response = self.client.post(
            "/sign_up/", self.data, content_type="application/json"
        )
        self.content = self._byte_content_to_dict(response.content)

    def _byte_content_to_dict(self, byte_content: bytes) -> dict:
        decode_content = byte_content.decode()
        dict_content = json.loads(decode_content)
        return dict_content

    def test_satus_content_username_with_valid_data(self):
        self.client.post("/sign_up/", self.data, content_type="application/json")
        user_content = self.content["user"]

        self.assertEqual(user_content["username"], "test_username")

    def test_satus_content_email_with_valid_data(self):
        self.client.post("/sign_up/", self.data, content_type="application/json")
        user_content = self.content["user"]

        self.assertEqual(user_content["email"], "test_email@test.com")

    def test_satus_content_gener_with_valid_data(self):
        self.client.post("/sign_up/", self.data, content_type="application/json")
        user_profile_content = self.content["user_profile"]

        self.assertEqual(user_profile_content["gender"], 1)

    def test_satus_content_description_with_valid_data(self):
        self.client.post("/sign_up/", self.data, content_type="application/json")
        user_profile_content = self.content["user_profile"]

        self.assertEqual(user_profile_content["description"], "test_description")
