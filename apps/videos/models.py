from django.db import models
from django.conf import settings
from apps.core.models import AbstractContent
from videos.managers import VideoManager
from videos.validators import validate_video_size
from channels.models import Channel


class Video(AbstractContent):
    """
    Model for saving videos.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="videos"
    )

    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name="videos"
    )

    objects = VideoManager()

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            # Validate the video size
            validate_video_size(file=self.file, user=self.user)
        return super().save(*args, **kwargs)
