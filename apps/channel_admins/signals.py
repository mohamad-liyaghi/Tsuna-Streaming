from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from channel_admins.models import ChannelAdmin, ChannelAdminPermission
from channel_subscribers.models import ChannelSubscriber
from apps.core.tasks import send_email


@receiver(post_save, sender=ChannelAdmin)
def send_admin_promotion_email(sender, created, instance, **kwargs):
    """
    Send email to admin after promotion.
    """
    if created:
        user = instance.user
        channel = instance.channel

        send_email(
            "emails/promotion_notification.html",
            to_email=user.email,
            body={
                "channel_title": channel.title,
                "first_name": user.first_name,
                "channel_token": channel.token
            }
        )

def create_admin_after_creating_channel(sender, created, instance, **kwargs):
    """
    Create admin after creating channel.
    """

    if created:

        ChannelAdmin .objects.create(user=instance.owner, channel=instance)


@receiver(post_delete, sender=ChannelSubscriber)
def delete_admin_after_unsubscribing(sender, **kwargs):
    """
    Delete admin after unsubscribing from channel.
    """
    instance = kwargs["instance"]
    ChannelAdmin.objects.filter(
        user=instance.user, channel=instance.channel
    ).delete()


@receiver(post_save, sender=ChannelAdmin )
def create_permissions_for_admin(sender, instance, created, *args, **kwargs):
    """
    Create permission object after an admin is created.
    """

    if created:
        ChannelAdminPermission.objects.create(
            admin=instance
        )
