from django.dispatch import receiver
from django.db.models.signals import post_save 
from django.conf import settings
from accounts.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token_for_new_user(sender, **kwargs):
    if kwargs["created"]:
        Token.objects.create(user=kwargs["instance"])