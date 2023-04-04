from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from v1.core.tasks import send_email
from videos.models import Video
from votes.signals import delete_object_votes_after_deleting
from comments.signals import delete_object_comments_after_deleting
from viewers.signals import delete_object_viewers_after_deleting


post_delete.connect(delete_object_votes_after_deleting, sender=Video)
post_delete.connect(delete_object_comments_after_deleting, sender=Video)
post_delete.connect(delete_object_viewers_after_deleting, sender=Video)



@receiver(post_save, sender=Video)
def notify_video_creation(sender, **kwargs):
    
    instance = kwargs["instance"]
    if not instance.pk:
            
        if instance.user == instance.channel.owner:
            send_email(template_name="emails/notify_video_creation.html", first_name=instance.user.first_name,
                        email=instance.user.email, channel_title=instance.title, video_token=instance.token)

        else:
            # send email to both admin and owner
            send_email(template_name="emails/notify_video_creation.html", first_name=instance.user.first_name,
                        email=instance.user.email, channel_title=instance.title, video_token=instance.token)

            send_email(template_name="emails/notify_video_creation.html", first_name=instance.user.first_name,
                        email=instance.channel.owner.email, channel_title=instance.title, video_token=instance.token)

