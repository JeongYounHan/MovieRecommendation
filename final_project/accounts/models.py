from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # 나를 팔로우 하는 사람 followers
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followings'
        
        )