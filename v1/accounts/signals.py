from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, pre_save
from django.conf import settings
from django.utils import timezone

from accounts.models import Token, Subscription, Plan
from config.tasks import send_email
from config.receivers import create_token_after_creating_object
import datetime

# create a unique token for object
pre_save.connect(create_token_after_creating_object, sender=settings.AUTH_USER_MODEL)
pre_save.connect(create_token_after_creating_object, sender=Subscription)
pre_save.connect(create_token_after_creating_object, sender=Token)
pre_save.connect(create_token_after_creating_object, sender=Plan)

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

        send_email.delay(template_name="emails/verification.html", email=user.email, first_name=user.first_name, 
                                        user_token=user.token, token=token.token)


@receiver(post_save, sender=Subscription)
def change_user_status_after_buying_premium_plan(sender, **kwargs):

    if kwargs["created"]:
        subscription = kwargs["instance"]
        user = subscription.user

        plan_active_months = subscription.plan.active_months
        finish_date = timezone.now() + datetime.timedelta(plan_active_months * 30)

        subscription.finish_date = finish_date
        subscription.save()
        
        if user.role != "a":
            user.role = "p"
            user.save()

        send_email.delay(template_name="emails/notify_premium.html", email=user.email, first_name=user.first_name, 
                                plan=subscription.plan.title, finish_date=subscription.finish_date)


@receiver(pre_delete, sender=Subscription)
def change_user_status_after_deleting_subscription(sender, **kwargs):
    '''Demote user when a subscription is deleted.'''
    subscription = kwargs["instance"]
    user = subscription.user
    
    if user.role != "a":
        user.role = "n"
        user.save()

    send_email.delay(template_name="emails/notify_unsubscribed_user.html", first_name=subscription.user.first_name,
                                email=subscription.user.email,
                                plan=subscription.plan.title, 
                                start_date=subscription.start_date)

