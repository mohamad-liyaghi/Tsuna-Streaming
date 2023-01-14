from django.dispatch import receiver
from django.db.models.signals import post_save 
from django.conf import settings
from accounts.models import Token
from accounts.tasks import send_email



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

        send_email.delay("verification", email=user.email, first_name=user.first_name, 
                                        user_id = user.user_id, token=token.token)