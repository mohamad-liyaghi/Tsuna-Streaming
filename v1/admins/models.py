from django.db import models
from channels.models import Channel
from accounts.models import Account


class Admin(models.Model):
    '''Base Channel Admin model'''

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='admin')
    promoted_by = models.ForeignKey(Account, on_delete=models.CharField, blank=True, null=True,
                                             related_name='promoted_admin')

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

    def save(self, *args, **kwargs):
        if not self.pk:

            # check admin exists or not
            if self.user.admin.filter(channel=self.channel).exists():
                raise ValueError("Admin already exists.")

            if self.user == self.channel.owner:
                return super(Admin, self).save(*args, **kwargs)

            if self.promoted_by.admin.filter(channel=self.channel, add_new_admin=True):
                return super(Admin, self).save(*args, **kwargs)
        
            raise ValueError("Permission denied to promote admin.")

        return super(Admin, self).save(*args, **kwargs)