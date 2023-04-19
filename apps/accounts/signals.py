from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from accounts.models import Token
from apps.core.tasks import send_email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        Token.objects.create(user=kwargs["instance"])


@receiver(post_save, sender=Token)
def send_token_via_email(sender, **kwargs):
    '''Signal to send token to user when the token created.'''

    if kwargs["created"]:

        token = kwargs["instance"]
        user = token.user

        send_email.delay(
            template_name="emails/token.html", 
            email=user.email, 
            first_name=user.first_name, 
            user_token=user.token, 
            token=token.token
        )

