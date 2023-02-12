from django.db import models
from django.conf import settings
from channels.models import Channel
from django.core.exceptions import ValidationError

class ChannelAdmin(models.Model):
    '''Channel admin model'''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                related_name="channel_admin")

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="admins")
    promoted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    token = models.CharField(max_length=32, null=True, blank=True)

    # permissions
    change_channel_info = models.BooleanField(default=False)
    add_new_admin = models.BooleanField(default=False)
    block_user = models.BooleanField(default=False)
    
    add_video = models.BooleanField(default=False)
    edit_video = models.BooleanField(default=False)
    delete_video = models.BooleanField(default=False)
    publish_video = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["channel", "user"],
                name="unique_channel_admin"
            )
        ]
    
    def __str__(self) -> str:
        return self.user.first_name
    

    def save(self, *args, **kwargs):

        if not self.pk:
            
            # check if user has subscribed to channel (before promoting as admin)
            if self.user.subscribed_channels.filter(channel=self.channel):
                return super(ChannelAdmin, self).save(*args, **kwargs)

            raise ValidationError("User hasnt subscribed your channel yet.")

        return super(ChannelAdmin, self).save(*args, **kwargs)