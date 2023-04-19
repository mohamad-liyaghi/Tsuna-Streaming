from django.utils import timezone
from accounts.models import Account, Token
from celery import shared_task
import datetime


@shared_task
def auto_delete_expired_tokens():
    '''Auto delete expired tokens from database'''
    
    # 10 mins before now
    ten_mins_before_now = timezone.now() - datetime.timedelta(minutes=10)
    # invalid tokens
    Token.objects.filter(date_created__lte=ten_mins_before_now).delete()



@shared_task
def auto_delete_deactive_users():
    '''Auto delete users that hasnt verified their accounts after a day.'''

    # one day before now
    a_day_before_now = timezone.now() - datetime.timedelta(1)

    # deactivated users
    Account.objects.filter(date_joined__lte=a_day_before_now, is_active=False).delete()

