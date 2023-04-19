from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError  
from apps.core.models import BaseContentModel
from channels.models import Channel
from videos.managers import VideoManager


class Video(BaseContentModel):

    video = models.FileField(upload_to="videos/user_video/")
    thumbnail = models.ImageField(upload_to="videos/thumbnail/", default="assets/images/default-video-thumbnail.jpg")


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="videos")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="videos")   

    objects = VideoManager()

    def __str__(self) -> str:
        return self.title

    def clean(self):
        file_size = self.video.size / (1024 * 1024)

        if self.user.role in ['a', 'p'] and file_size > 50:
            raise ValidationError('Video file size should not exceed 15MB.')
        
        if self.user.role == 'n' and file_size > 10:
            raise ValidationError('Normal users can upload videos up to 10MB.')

        super().clean()
    
    