from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import json

from src.user.models import UserProfileModel


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

    @staticmethod
    def byte_content_to_dict(byte_content: bytes) -> dict:
        decode_content = byte_content.decode()
        dict_content = json.loads(decode_content)
        return dict_content


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

    def test_creating_auth_token_after_registration(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Token.objects.count(), 0)

        self.client.post("/sign_up/", self.data, content_type="application/json")

        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(Token.objects.first().user, User.objects.first())

    def test_creating_user_profile_after_registration(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfileModel.objects.count(), 0)

        self.client.post("/sign_up/", self.data, content_type="application/json")

        self.assertEqual(UserProfileModel.objects.count(), 1)
        self.assertEqual(UserProfileModel.objects.first().user, User.objects.first())


class TestUserRegistrationPositiveResponseContent(UserRegistrationsTestCase):
    """
    Test cases for checking response content for valid post data.
    """

    def setUp(self) -> None:
        super().setUp()
        response = self.client.post(
            "/sign_up/", self.data, content_type="application/json"
        )
        self.content = self.byte_content_to_dict(response.content)

    def test_content_username_with_valid_data(self):
        self.client.post("/sign_up/", self.data, content_type="application/json")
        user_content = self.content["user"]

        self.assertEqual(user_content["username"], "test_username")

    def test_content_email_with_valid_data(self):
        self.client.post("/sign_up/", self.data, content_type="application/json")
        user_content = self.content["user"]

        self.assertEqual(user_content["email"], "test_email@test.com")

    def test_content_gener_with_valid_data(self):
        self.client.post("/sign_up/", self.data, content_type="application/json")
        user_profile_content = self.content["user_profile"]

        self.assertEqual(user_profile_content["gender"], 1)

    def test_content_description_with_valid_data(self):
        self.client.post("/sign_up/", self.data, content_type="application/json")
        user_profile_content = self.content["user_profile"]

        self.assertEqual(user_profile_content["description"], "test_description")


class TestUserRegistrationNegativeResponseContent(UserRegistrationsTestCase):
    """
    Test cases for checking response content for invalid post data.
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def input_json_data(
        self,
        username: str = "test_username",
        email: str = "test_email@test.com",
        password: str = "testpassword123!",
        password2: str = "testpassword123!",
        gender: int = 1,
        description: str = "test_description",
    ) -> str:
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "password2": password2,
        }
        user_pofile_data = {"gender": gender, "description": description}
        data = json.dumps(dict(user=user_data, user_profile=user_pofile_data))

        return data

    def test_content_without_username(self):
        data = self.input_json_data(username="")

        response = self.client.post("/sign_up/", data, content_type="application/json")
        self.content = self.byte_content_to_dict(response.content)
        expected_msg = "{'user': {'username': ['This field may not be blank.']}}"

        self.assertEqual(str(self.content), expected_msg)

    def test_content_without_email(self):
        data = self.input_json_data(email="")

        response = self.client.post("/sign_up/", data, content_type="application/json")
        self.content = self.byte_content_to_dict(response.content)
        expected_msg = "{'user': {'email': ['This field may not be blank.']}}"

        self.assertEqual(str(self.content), expected_msg)

    def test_content_with_existing_email(self):
        User.objects.create(
            username="test_username2",
            email="test_email@test.com",
            password="testpassword123!",
        )
        data = self.input_json_data()

        response = self.client.post("/sign_up/", data, content_type="application/json")
        self.content = self.byte_content_to_dict(response.content)
        expected_msg = "{'user': {'email': ['User with that email already exists']}}"

        self.assertEqual(str(self.content), expected_msg)

    def test_content_without_password(self):
        data = self.input_json_data(password="")

        response = self.client.post("/sign_up/", data, content_type="application/json")
        self.content = self.byte_content_to_dict(response.content)
        expected_msg = "{'user': {'password': ['This field may not be blank.']}}"

        self.assertEqual(str(self.content), expected_msg)

    def test_content_with_invalid_password(self):
        data = self.input_json_data(password="1234", password2="1234")

        response = self.client.post("/sign_up/", data, content_type="application/json")
        self.content = self.byte_content_to_dict(response.content)
        expected_msg = "{'user': {'password': ['This password is too short. It must contain at least 8 characters.', 'This password is too common.', 'This password is entirely numeric.']}}"
        print("Content: ", self.content)
        self.assertEqual(str(self.content), expected_msg)

    def test_content_with_not_same_passwords(self):
        data = self.input_json_data(password2="not_same_password")

        response = self.client.post("/sign_up/", data, content_type="application/json")
        self.content = self.byte_content_to_dict(response.content)
        expected_msg = "{'user': {'password': ['Password fields must be the same']}}"

        self.assertEqual(str(self.content), expected_msg)
