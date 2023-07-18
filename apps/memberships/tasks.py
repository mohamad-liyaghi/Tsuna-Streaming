from django.utils import timezone
from celery import shared_task
from memberships.models import Subscription


@shared_task
def auto_delete_invalid_subscription():
    """
    Delete expired subscriptions.
    """
    now = timezone.now()
    # Retrieve invalid subscriptions and delete them
    Subscription.objects.filter(end_date__lte=now).delete()
