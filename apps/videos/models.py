from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError  
from apps.core.models import AbstractContent
from channels.models import Channel
from videos.managers import VideoManager


class Video(AbstractContent):

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

    def clean(self):
        file_size = self.file.size / (1024 * 1024)

        if self.user.is_premium() and file_size > 50:
            raise ValidationError('Video file size should not exceed 15MB.')

        if self.user.is_normal() and file_size > 10:
            raise ValidationError('Normal users can upload videos up to 10MB.')

        super().clean()
