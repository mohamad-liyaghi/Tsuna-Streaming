from django.db import models
from django.conf import settings
from channels.models import Channel
from v1.accounts.utils import token_generator


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
    
    def __str__(self) -> str:
        return self.user.first_name
    

    
