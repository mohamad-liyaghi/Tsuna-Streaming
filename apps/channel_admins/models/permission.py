from django.db import models
from channel_admins.models import ChannelAdmin
from core.models import AbstractToken


class ChannelAdminPermission(AbstractToken):
    """
    Represents Permissions of a channel admin.
    """

    admin = models.OneToOneField(
        ChannelAdmin,
        on_delete=models.CASCADE,
        related_name='permissions'
    )

    # Permissions
    can_add_object = models.BooleanField(default=False)
    can_edit_object = models.BooleanField(default=False)
    can_delete_object = models.BooleanField(default=False)
    can_publish_object = models.BooleanField(default=False)
    can_change_channel_info = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.admin.user)

    PERMISSION_FIELDS = [
        'can_add_object',
        'can_edit_object',
        'can_delete_object',
        'can_publish_object',
        'can_change_channel_info',
    ]

    def save(self, *args, **kwargs):
        if not self.pk:
            # Set owner permission to True
            ChannelAdminPermission.set_owner_permission(
                admin=self
            )
        return super().save(*args, **kwargs)

    @classmethod
    def set_owner_permission(cls, admin) -> None:
        """
        If user is channel owner, set all permissions to True
        """
        if admin.admin.channel.owner == admin.admin.user:
            for field in cls.PERMISSION_FIELDS:
                setattr(admin, field, True)
