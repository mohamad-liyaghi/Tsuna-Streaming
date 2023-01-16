from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from templated_mail.mail import BaseEmailMessage
from celery import shared_task
import datetime
from django.utils import timezone


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

    elif type == "notify_premium":
        first_name = kwargs.get("first_name")   
        email = kwargs.get("email")   
        plan = kwargs.get("plan")   
        finish_date = kwargs.get("finish_date")   

        BaseEmailMessage(template_name="emails/notify_premium.html", 
                    context={"first_name" : first_name,
                                 "plan":plan, "finish_date" : finish_date}).send(to=[email])

    elif type == "notify_unsubscribed_user":
        first_name = kwargs.get("first_name")   
        email = kwargs.get("email")   
        plan = kwargs.get("plan")   
        start_date = kwargs.get("start_date")  
        print(first_name, email, plan, start_date) 

        BaseEmailMessage(template_name="emails/notify_unsubscribed_user.html", 
                    context={"first_name" : first_name,
                                 "plan":plan, "start_date" : start_date}).send(to=[email])
        

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

        if (user:=invalid_subscription.user).role == "p":
            user.role = "n"
            user.save()

        send_email.delay('notify_unsubscribed_user', first_name=invalid_subscription.user.first_name,
                                    email=invalid_subscription.user.email,
                                    plan=invalid_subscription.plan.title, 
                                    start_date=invalid_subscription.start_date)
        invalid_subscription.delete()
