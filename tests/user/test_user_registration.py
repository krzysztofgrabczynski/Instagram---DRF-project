from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import json


class TestUserRegistration(TestCase):
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

    def test_user_registration_with_valid_data(self):
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(
            "/sign_up/", self.data, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def _byte_content_to_dict(self, byte_content: bytes) -> dict:
        decode_content = byte_content.decode()
        dict_content = json.loads(decode_content)
        return dict_content

    def test_satus_content_with_valid_data(self):
        response = self.client.post(
            "/sign_up/", self.data, content_type="application/json"
        )
        content = self._byte_content_to_dict(response.content)
        user_content = content["user"]
        user_profile_content = content["user_profile"]

        self.assertEqual(user_content["username"], "test_username")
        self.assertEqual(user_content["email"], "test_email@test.com")
        self.assertEqual(user_profile_content["gender"], 1)
        self.assertEqual(user_profile_content["description"], "test_description")
