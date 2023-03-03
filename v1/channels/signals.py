from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from v1.core.tasks import send_email
from channels.models import Channel, ChannelSubscriber
from v1.core.receivers import create_token_after_creating_object

pre_save.connect(create_token_after_creating_object, sender=Channel)

@receiver(post_save, sender=Channel)
def notify_channel_creation(sender, **kwargs):
    '''Notify channel creation by email'''

    instance = kwargs["instance"]
    user = instance.owner

    if not instance.pk:
        send_email(template_name="emails/notify_channel_creation.html", first_name=user.first_name, email=user.email,
                                                        channel_title=instance.title, channel_token=instance.token)


@receiver(post_save, sender=Channel)
def create_subscriber_after_creating_channel(sender, **kwargs):
    '''Auto subscribe created channel by owner'''

    if kwargs["created"]:
        instance = kwargs["instance"]
        ChannelSubscriber.objects.create(channel=instance, user=instance.owner)
