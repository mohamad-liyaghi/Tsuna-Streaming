from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from memberships.models import Membership, Subscription
from v1.core.tasks import send_email


@receiver(post_save, sender=Subscription)
def notify_user_subscription(sender, **kwargs):

    if kwargs["created"]:
        subscription = kwargs["instance"]
        user = subscription.user

        send_email.delay(template_name="emails/notify_premium.html", email=user.email, first_name=user.first_name, 
                                plan=subscription.membership.title, finish_date=subscription.finish_date)


@receiver(pre_delete, sender=Subscription)
def notify_after_deleting_subscription(sender, **kwargs):
    '''Notify after deleting subscription'''

    subscription = kwargs["instance"]

    send_email.delay(template_name="emails/notify_unsubscribed_user.html", first_name=subscription.user.first_name,
                                email=subscription.user.email,
                                plan=subscription.membership.title, 
                                start_date=subscription.start_date)

