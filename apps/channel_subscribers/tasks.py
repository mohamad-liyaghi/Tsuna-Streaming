from django.core.cache import cache
from django.db.models import Q
from celery import shared_task
from channel_subscribers.models import ChannelSubscriber


CACHE_SUBSCRIBER_KEY = 'subscribers:*:*'


@shared_task
def insert_subscriber_from_cache_into_db():
    """
    Get all subscribers from cache and insert them into db
    """
    subscriber_keys = cache.keys(CACHE_SUBSCRIBER_KEY)
    # Get all subscribers from cache
    subscribers_in_cache = [
        cache.get(key) for key in subscriber_keys
    ]

    # Filter records with source of `cache` and status of `subscribed`
    cached_subscriber = filter(
        lambda subscriber: (
                subscriber.get('source') == 'cache'
                and
                subscriber.get('subscription_status') == 'subscribed'
        ),
        subscribers_in_cache
    )

    if cached_subscriber:
        # Bulk create subcribers and insert to db
        ChannelSubscriber.objects.bulk_create(
            [
                ChannelSubscriber(
                    channel=subscriber.get('channel'),
                    user=subscriber.get('user'),
                    date=subscriber.get('date'),
                ) for subscriber in cached_subscriber
            ]
        )
    # Remove subscribers from cache
    cache.delete_many(subscriber_keys)


@shared_task
def delete_unsubscribed_from_db():
    """
    Delete subscribers from db which
    their status is unsubscribed and source is cache
    """

    subscriber_keys = cache.keys(CACHE_SUBSCRIBER_KEY)
    # Retrieve all subscribers from cache
    subscribers_in_cache = [
        cache.get(key) for key in subscriber_keys
    ]

    # Filter records with status of `unsubscribed`
    cached_unsubscriber = filter(
        lambda subscriber: (
                subscriber.get('subscription_status') == 'unsubscribed'
        ),
        subscribers_in_cache
    )

    if cached_unsubscriber:
        # Zip the result (user, channel)
        zipped_user_channel = [
            (subscriber['user'], subscriber['channel'])
            for subscriber in cached_unsubscriber
        ]
        # Get users and channels
        users = [user for user, _ in zipped_user_channel]
        channels = [channel for _, channel in zipped_user_channel]

        # Delete unsubscribers from db
        ChannelSubscriber.objects.filter(
            Q(user__in=users) & Q(channel__in=channels)
        ).delete()

    # Remove unsubscribers from cache
    cache.delete_many(subscriber_keys)
