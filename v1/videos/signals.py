from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from v1.core.tasks import send_email
from videos.models import Video
from channels.models import ChannelAdmin
from votes.signals import delete_object_votes_after_deleting
from comments.signals import delete_object_comments_after_deleting
from viewers.signals import delete_object_viewers_after_deleting


post_delete.connect(delete_object_votes_after_deleting, sender=Video)
post_delete.connect(delete_object_comments_after_deleting, sender=Video)
post_delete.connect(delete_object_viewers_after_deleting, sender=Video)



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

