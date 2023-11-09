from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from accounts.models import VerificationToken
from apps.core.tasks import send_email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_verification_token(sender, created, instance, **kwargs):
    """Create token for user when user created."""
    # Check user is not active
    if created and not instance.is_active:
        VerificationToken.objects.create(user=instance)


@receiver(post_save, sender=VerificationToken)
def send_token_via_email(sender, created, **kwargs):
    """
    Send token via email when token created.
    """

    if created:
        token = kwargs["instance"]
        user = token.user

        send_email.delay(
            template_name="emails/verification_token.html",
            to_email=user.email,
            body={
                "first_name": user.first_name,
                "user_token": user.token,
                "token": token.token,
            },
        )
