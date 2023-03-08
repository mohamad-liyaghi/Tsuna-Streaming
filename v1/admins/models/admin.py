from django.db import models
from channels.models import Channel
from accounts.models import Account
from django.core.exceptions import PermissionDenied
from admins.exceptions import (DuplicatePromotionException, SubscriptionRequiredException)



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

            # only subscribed users can be promoted
            if not self.user.subscribed_channels.filter(channel=self.channel):
                raise SubscriptionRequiredException("User hasnt subscribed to channel.")

            # check admin exists or not
            if self.user.admin.filter(channel=self.channel).exists():
                raise DuplicatePromotionException("Admin already exists.")


            if self.user == self.channel.owner:
                return super(Admin, self).save(*args, **kwargs)    

            # user must have permission to promote an admin
            if not self.promoted_by.admin.filter(channel=self.channel, add_new_admin=True):
                raise PermissionDenied("Permission denied to promote admin.")
        
            return super(Admin, self).save(*args, **kwargs)    

        return super(Admin, self).save(*args, **kwargs)