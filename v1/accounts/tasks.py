from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from celery import shared_task
import datetime


@shared_task
def auto_delete_expired_tokens():
    '''Auto delete expired tokens from database'''
    
    # get the token model
    Token = ContentType.objects.get(app_label="accounts", model="token").model_class()
    # 10 mins before now
    ten_mins_before_now = timezone.now() - datetime.timedelta(minutes=10)
    # invalid tokens
    Token.objects.filter(date_created__lte=ten_mins_before_now).delete()



@shared_task
def auto_delete_deactive_users():
    '''Auto delete users that hasnt verified their accounts after a day.'''
    
    # get the account model
    Account = ContentType.objects.get(app_label="accounts", model="account").model_class()

    # one day before now
    a_day_before_now = timezone.now() - datetime.timedelta(1)

    # deactivated users
    Account.objects.filter(date_joined__lte=a_day_before_now, is_active=False).delete()


@shared_task
def auto_delete_invalid_subscription():
    '''Auto demote users that dont have premium plan anymore and delete their subscriptions'''
    # get Subscription model
    Subscription =  ContentType.objects.get(app_label="accounts", model="subscription").model_class()

    now = timezone.now()
    invalid_subscriptions = Subscription.objects.select_related('user').filter(finish_date__lte=now)

    for invalid_subscription in invalid_subscriptions:
        invalid_subscription.delete()
