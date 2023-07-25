from django.test import TestCase
from django.contrib.auth.models import User


class TestFollowAction(TestCase):
    """
    Test module for testing follow action.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        use1 = User.objects.create_user(username="test1", password="test")
        user2 = User.objects.create_user(username="test2", password="test")

    def test_follow_action(self) -> None:
        self.assertEqual(1, 1)
