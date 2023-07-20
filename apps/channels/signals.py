from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.core.tasks import send_email
from channels.models import Channel
from channel_subscribers.signals import create_subscriber_after_creating_channel
from channel_admins.signals import create_admin_after_creating_channel

# Create subscribers and admins after creating channel
post_save.connect(create_subscriber_after_creating_channel, sender=Channel)
post_save.connect(create_admin_after_creating_channel, sender=Channel)


@receiver(post_save, sender=Channel)
def notify_channel_creation(sender, instance, created, **kwargs):
    """
    Notify channel owner after creating channel
    """
    user = instance.owner

    if created:
        send_email(
            template_name="emails/notify_creation.html",
            to_email=user.email,
            body={
                "first_name": user.first_name,
                "channel_title": instance.title,
                "channel_token": instance.token
            }
        )
