from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, pre_save
from django.conf import settings
from django.utils import timezone

from accounts.models import Token
from v1.core.tasks import send_email
from v1.core.receivers import create_token_after_creating_object
import datetime


# create a unique token for object
pre_save.connect(create_token_after_creating_object, sender=settings.AUTH_USER_MODEL)
pre_save.connect(create_token_after_creating_object, sender=Token)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        Token.objects.create(user=kwargs["instance"])


@receiver(post_save, sender=Token)
def send_email_when_token_created(sender, **kwargs):
    '''
        After creating a user, a token gets created.
        After that this signal emails that token.
    '''

    if kwargs["created"]:
        token = kwargs["instance"]
        user = token.user

        send_email.delay(template_name="emails/verification.html", email=user.email, first_name=user.first_name, 
                                        user_token=user.token, token=token.token)

