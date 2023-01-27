from django.db import models
from django.conf import settings
from channels.models import Channel
from videos.utils import video_token_generator


class Video(models.Model):

    class Visibility(models.TextChoices):
        PRIVATE = ("pr", "Private")
        PUBLISHED = ("pu", "Public")

    title = models.CharField( max_length=100)
    description = models.TextField(max_length=300)

    video = models.FileField(upload_to="videos/user_video/")
    thumbnail = models.ImageField(upload_to="videos/thumbnail/", default="media/default-video-thumbnail.jpg")

    token = models.CharField(max_length=32, default=video_token_generator)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="videos")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="videos")   
    date = models.DateTimeField(auto_now_add=True)

    visibility = models.CharField(max_length=2, choices=Visibility.choices, default=Visibility.PRIVATE)
    is_updated = models.BooleanField(default=False)


    @property
    def is_published(self):
        return self.visibility == "pu"
