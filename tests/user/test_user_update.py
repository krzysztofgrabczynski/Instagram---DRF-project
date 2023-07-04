from django.test import TestCase
from django.contrib.auth.models import User

from src.user.models import UserProfileModel


class TestUserAccountUpdate(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user_data = {
            "username": "test_user",
            "email": "test@email.com",
            "password": "test_password",
        }
        user = User.objects.create_user(**user_data)
        UserProfileModel.objects.create(user=user, description="test_description")

    
        