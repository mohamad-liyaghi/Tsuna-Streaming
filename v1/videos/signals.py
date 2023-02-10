from django.dispatch import receiver
from django.db.models.signals import pre_save
from config.tasks import send_email
from videos.models import Video
from channels.models import ChannelAdmin

@receiver(pre_save, sender=Video)
def add_video_access_and_notify(sender, **kwargs):
    '''Check if user is chanenl owner or admin in order to add a video'''
    
    instance = kwargs["instance"]
    if not instance.pk:
        if  instance.user == instance.channel.owner or  \
            ChannelAdmin.objects.filter(channel=instance.channel, user=instance.user, add_video=True).exists():
        
            if instance.user == instance.channel.owner:
                send_email(template_name="emails/notify_after_creating_video.html", first_name=instance.user.first_name,
                            email=instance.user.email, channel_title=instance.title, video_token=instance.token)

            else:
                # send email to both admin and owner
                send_email(template_name="emails/notify_after_creating_video.html", first_name=instance.user.first_name,
                            email=instance.user.email, channel_title=instance.title, video_token=instance.token)

                send_email(template_name="emails/notify_after_creating_video.html", first_name=instance.user.first_name,
                            email=instance.channel.owner.email, channel_title=instance.title, video_token=instance.token)

        else:
            raise ValueError("Permission denied")