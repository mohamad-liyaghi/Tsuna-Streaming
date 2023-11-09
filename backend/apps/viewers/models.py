from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from viewers.managers import ViewerManager
from channels.models import Channel


class Viewer(models.Model):
    """
    Model for tracking views of any object.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = ViewerManager()

    def __str__(self) -> str:
        return str(self.user)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.__set_channel()
        super().save(*args, **kwargs)

    def __set_channel(self) -> None:
        self.channel = self.content_object.channel
