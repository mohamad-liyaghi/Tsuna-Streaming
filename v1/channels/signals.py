from django.dispatch import receiver
from django.db.models.signals import pre_save
from accounts.tasks import send_email
from channels.models import Channel

@receiver(pre_save, sender=Channel)
def check_channel_limit_and_notify(sender, **kwargs):
    '''Check channel limits, create channel and notify'''
    instance = kwargs["instance"]
    # check if object is not getting update
    if not instance.pk:
        user = instance.owner

        if user.role in ["a", "p"]:
            # premium users can have 10 channels
            if user.channels.count() < 10:
                send_email(template_name="emails/notify_channel_creation.html", first_name=user.first_name, email=user.email,
                                                        channel_title=instance.title, channel_token=instance.token)
            else:
                raise ValueError("Premium users can not have more that 10 channels")

        else:
            
            # Check for users that had created a channel when they were premium
            if user.channels.count() > 5 and user.channels.count() < 10:
                send_email(template_name="emails/notify_channel_creation.html", first_name=user.first_name, email=user.email,
                                                        channel_title=instance.title, channel_token=instance.token)

            # normal users can have 5 channels [Exept the ones who has purchased membership]
            elif user.channels.count() < 5:
                send_email(template_name="emails/notify_channel_creation.html", first_name=user.first_name, email=user.email,
                                                        channel_title=instance.title, channel_token=instance.token)
            else:
                raise ValueError("Normal users can not have more that 5 channels")