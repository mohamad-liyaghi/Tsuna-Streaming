from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from memberships.models import Membership, Subscription
from apps.core.tasks import send_email


@receiver(post_save, sender=Subscription)
def notify_user_subscription(sender, created, instance, **kwargs):
    """
    Norify a user when a new subscription is created for him
    """

    if created:
        subscription = instance
        user = subscription.user

        send_email.delay(
            template_name="emails/notify_premium.html", 
            to_email=user.email,
            body={
                "first_name": user.first_name,
                "membership_title": subscription.membership.title,
                "end_date": subscription.end_date
            }
        )


@receiver(pre_delete, sender=Subscription)
def notify_user_plan_expiration(sender, instance, **kwargs):
    """
    Notify a user when his subscription is expired
    """

    subscription = instance

    send_email.delay(
        template_name="emails/notify_plan_expiration.html", 
        to_email=subscription.user.email,
        body={
            "first_name": subscription.user.first_name,
        }
    )
