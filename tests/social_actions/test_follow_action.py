from django.test import TestCase
from django.contrib.auth.models import User


from tests.user.test_user_update import TestUserUpdateGeneric
from src.user.models import UserProfileModel
from src.social_actions.models import LikeModel, FollowModel


class TestFollowAction(TestUserUpdateGeneric):
    """
    Test module for testing follow action.
    Parent class TestUserUpdateGeneric provides setUpTestData and setUp method with creating two users with profiles and tokens.
    """

    def test_following_between_two_users(self) -> None:
        response = self.client.get(
            f"/user_profile/{self.user_profile2.id}/follow_action/"
        )
        update_user_profile = UserProfileModel.objects.get(user=self.user)
        update_user_profile2 = UserProfileModel.objects.get(user=self.user2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_user_profile.following_amount, 1)
        self.assertEqual(update_user_profile2.followers_amount, 1)
        self.assertEqual(FollowModel.objects.count(), 1)

    def test_unfollowing_between_two_users(self) -> None:
        FollowModel.objects.create(user=self.user, user_followed=self.user2)
        update_user_profile = UserProfileModel.objects.get(user=self.user)
        update_user_profile2 = UserProfileModel.objects.get(user=self.user2)
        update_user_profile.following_amount += 1
        update_user_profile.save()
        update_user_profile2.followers_amount += 1
        update_user_profile2.save()
        self.assertEqual(FollowModel.objects.count(), 1)
        self.assertEqual(update_user_profile.following_amount, 1)
        self.assertEqual(update_user_profile2.followers_amount, 1)

        response = self.client.get(
            f"/user_profile/{self.user_profile2.id}/follow_action/"
        )
        update_user_profile = UserProfileModel.objects.get(user=self.user)
        update_user_profile2 = UserProfileModel.objects.get(user=self.user2)
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(update_user_profile.following_amount, 0)
        self.assertEqual(update_user_profile2.followers_amount, 0)
        self.assertEqual(FollowModel.objects.count(), 0)

    def test_following_own_profile(self) -> None:
        response = self.client.get(
            f"/user_profile/{self.user_profile.id}/follow_action/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(FollowModel.objects.count(), 0)
