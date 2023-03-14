from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from memberships.models import Membership, Subscription
from v1.core.receivers import create_token_after_creating_object
from v1.core.tasks import send_email

# create unique token for each object
pre_save.connect(create_token_after_creating_object, sender=Membership)
pre_save.connect(create_token_after_creating_object, sender=Subscription)


@receiver(post_save, sender=Subscription)
def notify_user_subscription(sender, **kwargs):

    if kwargs["created"]:
        subscription = kwargs["instance"]
        user = subscription.user

        send_email.delay(template_name="emails/notify_premium.html", email=user.email, first_name=user.first_name, 
                                plan=subscription.membership.title, finish_date=subscription.finish_date)