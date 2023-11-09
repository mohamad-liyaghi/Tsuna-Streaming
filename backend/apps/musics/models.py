from django.db import models
from django.conf import settings
from musics.validators import validate_music_size
from contents.models import AbstractContent
from channels.models import Channel


class Music(AbstractContent):
    """
    Main model for music content.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="musics"
    )

    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="musics"
    )

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        # Validate music size
        validate_music_size(file=self.file, user=self.user)
        return super().save(*args, **kwargs)
