from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from memberships.models import Membership, Subscription
from apps.core.tasks import send_email


@receiver(post_save, sender=Subscription)
def notify_user_subscription(sender, created, instance, **kwargs):
    '''Notify a user by email that the subscription has just started'''

    if created:

        subscription = instance
        user = subscription.user

        send_email.delay(
            template_name="emails/notify_premium.html", 
            email=user.email, 
            first_name=user.first_name, 
            membership_title=subscription.membership.title, 
            finish_date=subscription.finish_date
        )


@receiver(pre_delete, sender=Subscription)
def notify_user_plan_expiration(sender, instance, **kwargs):
    '''Notify after deleting subscription'''

    subscription = instance

    send_email.delay(
        template_name="emails/notify_plan_expiration.html", 
        first_name=subscription.user.first_name,
        email=subscription.user.email, 
    )

