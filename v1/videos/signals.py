from django.dispatch import receiver
from django.db.models.signals import pre_save
from videos.models import Video
from channels.models import ChannelAdmin

@receiver(pre_save, sender=Video)
def add_video_access_and_notify(sender, **kwargs):
    '''Check if user is chanenl owner or admin in order to add a video'''
    
    instance = kwargs["instance"]
    
    if not instance.pk:
        if not instance.user == instance.channel.owner or\
            ChannelAdmin.objects.filter(channel=instance.channel, user=instance.user).exists():
            raise ValueError("Permission denied")

