from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from config.tasks import send_email
from channels.models import Channel, ChannelAdmin, ChannelSubscriber

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



@receiver(pre_save, sender=ChannelAdmin)
def check_and_notify_after_promoting_admin(sender, **kwargs):
    instance = kwargs["instance"]
    
    if not instance.pk:
        user = instance.user
        promoted_by = instance.promoted_by
        channel = instance.channel
        
        if ChannelAdmin.objects.filter(user=user, channel=channel, promoted_by=promoted_by).exists():
            raise ValueError("Admin already exists")

        # check if user has permission to promote an admin
        if channel.owner == promoted_by or \
                promoted_by.channel_admin.filter(user=promoted_by, add_new_admin=True):

                send_email("emails/notify_user_after_promoting.html", email=user.email,
                            channel=channel.title, first_name=user.first_name, channel_token=channel.token)
        
        else:
            raise ValueError("Permission denied for promoting in this channel.")



@receiver(post_save, sender=Channel)
def create_subscriber_after_creating_channel(sender, **kwargs):
    '''Auto subscribe created channel by owner'''
    if kwargs["created"]:
        instance = kwargs["instance"]
        ChannelSubscriber.objects.create(channel=instance, user=instance.owner)


@receiver(post_delete, sender=ChannelSubscriber)
def delete_admin_after_unsubscribing(sender, **kwargs):
    instance = kwargs["instance"]
    
    if (admin:=ChannelAdmin.objects.filter(user=instance.user, channel=instance.channel)):
        admin.delete()
