from django.core.cache import cache
from celery import shared_task
from channel_subscribers.models import ChannelSubscriber
from accounts.models import Account
from channel_subscribers.models import Channel


@shared_task
def insert_subscriber_from_cache_into_db():
    subscriber_keys = cache.keys("subscriber:*:*")

    if subscriber_keys:
        for key in subscriber_keys:
            subscriber = cache.get(key)
            _, channel_token, user_token = key.split(':') # subscriber:channel_token:user_token
            
            if (subscriber and subscriber.get('subscription_status', '') == 'subscribed' 
                    and subscriber.get('source', '') == 'cache'):
                try:
                    # Create channel subscriber
                    ChannelSubscriber.objects.create(
                        channel = Channel.objects.get(token=channel_token), 
                        user = Account.objects.get(token=user_token),
                        date = subscriber.get('date'),
                    )
                    subscriber['source'] = 'database'
                    cache.set(key, subscriber)

                except:
                    # Delete subscriber if operation failed
                    cache.delete(key)