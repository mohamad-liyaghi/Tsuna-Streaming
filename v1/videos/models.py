from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError  
from django.contrib.contenttypes.fields import GenericRelation
from v1.core.models import BaseContentModel
from channels.models import Channel
from videos.managers import VideoManager
from votes.models import Vote
from comments.models import Comment
from viewers.models import Viewer

class Video(BaseContentModel):

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)

    video = models.FileField(upload_to="videos/user_video/")
    thumbnail = models.ImageField(upload_to="videos/thumbnail/", default="assets/images/default-video-thumbnail.jpg")


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="videos")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="videos")   

    objects = VideoManager()

    @property
    def is_published(self):
        return self.visibility == "pu"

    def __str__(self) -> str:
        return self.title

    def clean(self):
        '''Check video size. Normal users can upload 20Mb videos and premiums can upload 50.'''
        if self.video.size > 5242880:
            raise ValidationError("File size must be less than 50MB.")

        if self.user.role in ['a', 'p']:
            if self.video.size <= 5242880:
                return super().clean()
            raise ValidationError("File size must be less than 50MB.")

        if self.video.size <= 20971520:
            return super().clean()

        raise ValidationError("File size must be under 20MB.")
    
    