from django.db import models
from channels.models import Channel
from accounts.models import Account


class Admin(models.Model):
    '''Base Channel Admin model'''

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='admin')
    promoted_by = models.ForeignKey(Account, on_delete=models.CharField, related_name='promoted_admin')

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='admins')

    date = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=32, null=True, blank=True)

    # Basic channel permissions
    change_channel_info = models.BooleanField(default=False)
    add_new_admin = models.BooleanField(default=False)
    block_user = models.BooleanField(default=False)


    @property
    def is_owner(self):
        return bool(self.user == self.channel.owner)

    def __str__(self) -> str:
        return str(self.user)
    
    class Meta:
        # Avoid admin duplication

        constraints = [
            models.UniqueConstraint(
                fields=["channel", "user"],
                name="unique_channel_admins"
            )
        ]

