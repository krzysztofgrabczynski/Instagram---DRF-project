from django.test import TestCase
from django.contrib.auth.models import User
import pytest

from src.user.models import UserProfileModel


class TestUserProfileModel(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        User.objects.create_user(username="test", password="test")

        UserProfileModel.objects.create(user=User.objects.get(username="test"))

    def test_str_method(self):
        user = User.objects.get(username="test")
        user_profile = UserProfileModel.objects.first()
        expected = f"Profile(id:{user_profile.id}): {user.username}(id:{user.id})"

        self.assertEqual(expected, str(user_profile))
