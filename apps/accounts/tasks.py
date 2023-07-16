from django.utils import timezone
from accounts.models import Account, VerificationToken
from celery import shared_task
import datetime


@shared_task
def auto_delete_expired_tokens():
    '''Auto delete expired tokens from database'''

    now = timezone.now()

    # invalid tokens
    VerificationToken.objects.filter(
        expire_at__lte=now
    ).delete()


@shared_task
def auto_delete_deactive_users():
    '''Auto delete users that hasnt verified their accounts after a day.'''

    # one day before now
    a_day_before_now = timezone.now() - datetime.timedelta(1)

    # deactivated users
    Account.objects.filter(date_joined__lte=a_day_before_now, is_active=False).delete()

