from django.db import models
from channel_admins.models import ChannelAdmin
from core.models import AbstractToken


class ChannelAdminPermission(AbstractToken):
    """
    Represents Permissions of a channel admin.
    """

    admin = models.ForeignKey(
        ChannelAdmin,
        on_delete=models.CASCADE,
        related_name='permissions'
    )

    # Permissions
    add_object = models.BooleanField(default=False)
    edit_object = models.BooleanField(default=False)
    delete_object = models.BooleanField(default=False)
    publish_object = models.BooleanField(default=False)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["admin", "model"],
                name="unique_admin_permission"
            )
        ]

    def __str__(self) -> str:
        return str(self.admin.user)

    PERMISSION_FIELDS = [
        'add_object',
        'edit_object',
        'delete_object',
        'publish_object'
    ]

    def save(self, *args, **kwargs):
        if not self.pk:
            # Set owner permission to True
            ChannelAdminPermission.set_owner_permission(
                admin=self.admin
            )
        return super().save(*args, **kwargs)

    @classmethod
    def set_owner_permission(cls, admin) -> None:
        """
        If user is channel owner, set all permissions to True
        """
        if admin.channel.owner == admin.user:
            for field in cls.PERMISSION_FIELDS:
                setattr(admin, field, True)
