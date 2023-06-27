from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UserProfileModel(models.Model):
    """
    Django model for user's profile/bio.
    """

    class gender_choices(models.IntegerChoices):
        MALE = 0
        FEMALE = 1

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.PositiveSmallIntegerField(
        choices=gender_choices.choices, default=gender_choices.MALE
    )
    description = models.TextField(default="", blank=True)
    profile_img = models.ImageField(
        default="profile_imgs/default_male.jpg",
        upload_to="profile_imgs",
        blank=True,
        null=True,
    )
    posts_amount = models.IntegerField(default=0)
    followers_amount = models.IntegerField(default=0)
    following_amount = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Profile(id:{self.id}): {self.user.username}(id:{self.user.id})"

    def __repr__(self) -> str:
        return self.__str__()
