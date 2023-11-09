from django.utils import timezone
from accounts.models import Account, VerificationToken
from celery import shared_task
import datetime


@shared_task
def auto_delete_expired_tokens():
    """
    Auto delete expired tokens.
    """

    now = timezone.now()

    # invalid tokens
    VerificationToken.objects.filter(expire_at__lte=now).delete()


@shared_task
def auto_delete_deactive_users():
    """
    Auto delete deactive users after one day.
    """

    # one day before now
    yesterday = timezone.now() - datetime.timedelta(1)

    # deactivated users
    Account.objects.filter(date_joined__lte=yesterday, is_active=False).delete()
