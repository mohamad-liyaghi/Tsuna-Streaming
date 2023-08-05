from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from apps.core.tasks import send_email
from videos.models import Video


@receiver(post_save, sender=Video)
def notify_video_creation(sender, instance, created, **kwargs):
    """
    Notify Both uploader and channel owner.
    """
    
    if created:

        data = {
            "first_name": instance.user.first_name,
            "channel_title": instance.title,
            "video_token": instance.token,
            "channel_token": instance.channel.token,
        }

        if instance.user == instance.channel.owner:
            send_email.delay(
                template_name="emails/notify_video_creation.html",
                to_email=instance.user.email,
                body={**data}
            )

        else:
            # send email to both admin and owner
            send_email.delay(
                template_name="emails/notify_video_creation.html",
                to_email=instance.user.email,
                body={**data}
            )

            send_email.delay(
                template_name="emails/notify_video_creation.html",
                to_email=instance.channel.owner.email,
                body={**data}
            )
