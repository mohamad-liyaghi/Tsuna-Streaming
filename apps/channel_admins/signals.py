from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete

from channel_admins.models import ChannelAdmin , ChannelAdminPermission
from channel_subscribers.models import ChannelSubscriber
from apps.core.tasks import send_email
from channel_admins.tasks import create_permission_for_admin


@receiver(post_save, sender=ChannelAdmin)
def send_admin_promotion_email(sender, **kwargs):
    '''Notify a user when has been promoted'''

    instance = kwargs["instance"]
    
    if kwargs['created']:
        user = instance.user
        channel = instance.channel

        send_email(
            "emails/promotion_notification.html", 
            email=user.email,
            channel_title=channel.title, 
            first_name=user.first_name, 
            channel_token=channel.token
        )
        

def create_admin_after_creating_channel(sender, **kwargs):
    '''Auto admin created channel by owner'''

    if kwargs["created"]:
        instance = kwargs["instance"]

        ChannelAdmin .objects.create(
            user=instance.owner, channel=instance, 
            change_channel_info = True, add_new_admin = True, block_user = True
        )


@receiver(post_delete, sender=ChannelSubscriber)
def delete_admin_after_unsubscribing(sender, **kwargs):
    instance = kwargs["instance"]
    
    if (admin:=instance.user.channel_admins.filter(channel=instance.channel)):
        admin.delete()



@receiver(post_save, sender=ChannelAdmin )
def create_permissions_for_admin(sender, instance, *args, **kwargs):
    '''
        Create permission for admin after an admin gets created.
        Permissions for all Content classes. E.g: Video.
    '''

    if kwargs['created']:

        # call the function to create permissions and pass admin token/
        create_permission_for_admin.delay(str(instance.token))