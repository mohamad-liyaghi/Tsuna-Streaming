from templated_mail.mail import BaseEmailMessage
from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import datetime



@shared_task
def send_email(type, **kwargs):
    '''This email task can be used for email verification and other purposes'''

    if type == "verification":
        
        first_name = kwargs.get("first_name")    
        user_id = kwargs.get("user_id")    
        token = kwargs.get("token")    
        email = kwargs.get("email")

        BaseEmailMessage(template_name="emails/verification.html", 
                    context={"first_name" : first_name, "user_id" : user_id,
                                 "token" : token}).send(to=[email])


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
