from django.db import models
from django.conf import settings
from accounts.validators import validate_profile_size
from channels.utils import channel_token_generator


class Channel(models.Model):
    title = models.CharField(max_length=240)
    description = models.TextField(max_length=500, default="A new channel on Tsuna Streaming.")

    profile = models.ImageField(upload_to="channels/profile", default="media/images/default-channel-profile.jpg",
                                    validators=[validate_profile_size,])

    thumbnail = models.ImageField(upload_to="channels/profile", default="media/images/default-thumbnail.jpg",
                                    validators=[validate_profile_size,])
    
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                related_name="channels")

    token = models.CharField(max_length=32, unique=True, default=channel_token_generator)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title