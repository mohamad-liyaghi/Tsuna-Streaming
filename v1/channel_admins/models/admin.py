from django.db import models
from channels.models import Channel
from channel_subscribers.models import ChannelSubscriber
from accounts.models import Account
from django.core.exceptions import PermissionDenied
from channel_admins.exceptions import (DuplicatePromotionException, SubscriptionRequiredException)
from core.models import BaseTokenModel


class ChannelAdmin(BaseTokenModel):
    '''Base Channel Admin model'''

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='channel_admins')
    promoted_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True,
                                             related_name='promoted_admins')

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='admins')

    date = models.DateTimeField(auto_now_add=True)

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
                name="unique_channel_admin"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            subscriber = ChannelSubscriber.objects.get_from_cache(
                    channel_token=self.channel.token, user_token=self.user.token
                )

            # Raise error if use hasnt subscribed to channel
            if not subscriber:
                raise SubscriptionRequiredException("User hasnt subscribed to channel.")
            
            if subscriber and not ChannelSubscriber.objects.filter(channel=self.channel, user=self.user):
                raise SubscriptionRequiredException("User must be subscribed to channel for at least 24 hours to get promoted.")

            # check admin exists or not
            if self.user.channel_admins.filter(channel=self.channel).exists():
                raise DuplicatePromotionException("Admin already exists.")

            if self.user == self.channel.owner:
                return super(ChannelAdmin, self).save(*args, **kwargs)    

            # user must have permission to promote an admin
            if not self.promoted_by.channel_admins.filter(channel=self.channel, add_new_admin=True):
                raise PermissionDenied("Permission denied to promote admin.")
        
            return super(ChannelAdmin, self).save(*args, **kwargs)    

        return super(ChannelAdmin, self).save(*args, **kwargs)