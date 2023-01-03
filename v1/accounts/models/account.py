from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):

    class Role(models.TextChoices):
        '''User Role'''
        ADMIN = ("a", "Admin")
        PREMIUM = ("p", "Premium")
        NORMAL = ("n", "Normal")

    username = None
    email = models.EmailField(max_length=200, unique=True)

    picture = models.ImageField(upload_to="accounts/profile")

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    bio = models.TextField(max_length=250)

    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=1, choices=Role.choices, default=Role.NORMAL)

    user_id = models.CharField(max_length=15)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "bio"]

    def __str__(self) -> str:
        return self.user_id

    class Meta:
        app_label = "accounts"
        db_table = 'accounts_account'


    