from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError  
from apps.core.models import AbstractContent
from channels.models import Channel


class Music(AbstractContent):
    '''
        The main Music model that uses common fields of AbstractContent
    '''

    music = models.FileField(upload_to="musics/user_music/")
    thumbnail = models.ImageField(upload_to="musics/thumbnail/", default="assets/images/default-music-thumbnail.jpg")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="musics")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="musics")   

    def __str__(self) -> str:
        return self.title

    def clean(self):
        '''Check the file size and raise error if it is more that expected size.'''
        file_size = self.music.size / (1024 * 1024)

        if self.user.role in ['a', 'p'] and file_size > 15:
            raise ValidationError('Music file size should not exceed 15MB.')
        
        if self.user.role == 'n' and file_size > 10:
            raise ValidationError('Normal users can upload music files up to 10MB.')

        super().clean()