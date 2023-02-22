from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from v1.core.tasks import send_email
from channels.models import Channel, ChannelSubscriber
from core.receivers import create_token_after_creating_object
from admins.models import Admin, Permission

pre_save.connect(create_token_after_creating_object, sender=Admin)
pre_save.connect(create_token_after_creating_object, sender=Permission)

@receiver(pre_save, sender=Admin)
def notify_after_promoting_admin_admin(sender, **kwargs):
    instance = kwargs["instance"]
    
    if not instance.pk:
        user = instance.user
        channel = instance.channel

        send_email("emails/notify_user_after_promoting.html", email=user.email,
                    channel=channel.title, first_name=user.first_name, channel_token=channel.token)
        

@receiver(post_save, sender=Channel)
def create_admin_after_creating_channel(sender, **kwargs):
    '''Auto admin created channel by owner'''

    if kwargs["created"]:
        instance = kwargs["instance"]

        Admin.objects.create(
            user=instance.owner, channel=instance, 
            change_channel_info = True, add_new_admin = True, block_user = True
        )


@receiver(post_delete, sender=ChannelSubscriber)
def delete_admin_after_unsubscribing(sender, **kwargs):
    instance = kwargs["instance"]
    
    if (admin:=instance.user.admin.filter(channel=instance.channel)):
        admin.delete()