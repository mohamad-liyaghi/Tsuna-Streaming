from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.db.models import BooleanField
from celery import shared_task
from v1.core.models import BaseContentModel
from admins.models import Admin, Permission



@shared_task
def create_permission_for_admin(admin_token, *args, **kwargs):
    '''When an admin gets created, a signal gets called and permissions for that admin will be created.'''

    # get all boolean fields related to Permission class
    # fields will be used for owner/admin permissions.
    permission_boolean_fields = list(
                                    # filter fields that are BooleanField.
                                    # boolean fields are all permissions like add_object.
                                    filter(lambda x: type(x) == BooleanField, Permission._meta.get_fields())
                                )

    # all content models (e.g: Video, etc.)
    content_models = BaseContentModel.__subclasses__()

    # get the admin that got created.
    if (admin:= Admin.objects.filter(token=admin_token).first()):

        # By default channel owmers have all the permissions.
        # if user is owner, this funntion returns True by default.
        check_user_ownership = lambda: bool(admin.channel.owner == admin.user)

        with transaction.atomic():
            # create permission for all content models 

            for content_model in content_models:
                # get the Content model instance (E.g: video model)
                Klass = ContentType.objects.get(model=content_model.__name__.lower())
                
                # Default valued for permissions
                # if user is owner, check_user_ownership returns True and all the permissions will be given.
                boolean_field = {field.name:check_user_ownership() for (field) in permission_boolean_fields}

                # create permission for the admin and the channel.
                Permission.objects.create(admin=admin, model=Klass, **boolean_field)

