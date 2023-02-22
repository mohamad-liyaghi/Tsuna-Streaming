from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from django.db import transaction
from django.contrib.contenttypes.models import ContentType

from admins.models import Admin, Permission
from channels.models import Channel, ChannelSubscriber
from v1.core.receivers import create_token_after_creating_object
from v1.core.models import BaseContentModel
from v1.core.tasks import send_email


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


@receiver(post_save, sender=Admin)
def create_permission_for_admin(sender, instance, *args, **kwargs):
    '''Create permissionf or all Content models (Video, community etc...) when a users gets created.'''

    if kwargs['created']:

        # content models are Video, Posts and stuff
        content_models = BaseContentModel.__subclasses__()

        admin = instance    
    
        # if user is channels admin, by default all the permissions are given.
        set_default_permission = lambda: bool(admin.channel.owner == admin.user)

        default_permissions = {
            "add_object" : set_default_permission(),
            "edit_object" : set_default_permission(),
            "delete_object" : set_default_permission(),
            "publish_object" : set_default_permission(),
        }

        with transaction.atomic():
            # create permission for all content models 

            for content_model in content_models:
                model = ContentType.objects.get(model=content_model.__name__.lower())
                Permission.objects.create(admin=admin, model=model, **default_permissions)


        