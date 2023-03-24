from django.core.cache import cache
from celery import shared_task
from channel_subscribers.models import ChannelSubscriber
from accounts.models import Account
from channel_subscribers.models import Channel


@shared_task
def insert_subscriber_from_cache_into_db():
    '''Insert subscribers that are in cache'''
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


@shared_task
def delete_unsubscribed_from_db():
    '''Delete users that has unsubscribed a channel from db'''

    subscriber_keys = cache.keys("subscriber:*:*")

    if subscriber_keys:
        for key in subscriber_keys:
            subscriber = cache.get(key)
            _, channel_token, user_token = key.split(':') # subscriber:channel_token:user_token
            
            # If subscriber status is unsubscribed and source is in cache
            # Get and delete sub
            if (subscriber and subscriber.get('subscription_status', '') == 'unsubscribed' 
                    and subscriber.get('source', '') == 'cache'):
                try:
                    # Create channel subscriber
                    ChannelSubscriber.objects.get(
                        channel__token = channel_token,
                        user__token = user_token,
                    ).delete()

                except:
                    pass

                cache.delete(key)