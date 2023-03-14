from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from celery import shared_task


@shared_task
def auto_delete_invalid_subscription():
    '''
        Deletes invalid subscriptions where finish_date <= current date/time
    '''

    # get Subscription model
    Subscription =  ContentType.objects.get(app_label="memberships", model="subscription").model_class()

    now = timezone.now()

    # Retrieve invalid subscriptions and delete them
    Subscription.objects.filter(finish_date__lte=now).delete()