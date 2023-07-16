from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.validators import validate_profile_size
from accounts.managers import AccountManager
from .role import AbstractAccountRole
from core.models import AbstractToken


class Account(AbstractUser, AbstractToken, AbstractAccountRole):
    username = None
    email = models.EmailField(max_length=200, unique=True)

    picture = models.ImageField(
        upload_to="accounts/profile",
        default="assets/images/default-user-profile.jpg",
        validators=[validate_profile_size]
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    bio = models.TextField(
        max_length=250,
        blank=True,
        default="Hey there, i am using tsuna streaming."
    )

    is_active = models.BooleanField(default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "bio"]

    objects = AccountManager()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self) -> str:
        """Concatenate first name and last name"""
        return f'{self.first_name} {self.last_name}'

    class Meta:
        app_label = "accounts"
        db_table = 'accounts_account'


    