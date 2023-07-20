from django.db import models
from django.conf import settings
from django.core.cache import cache
from channels.models import Channel
from channel_subscribers.managers import ChannelSubscriberManager


class ChannelSubscriber(models.Model):
    """Model to represent a user's subscription to a channel."""
    
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name="subscribers"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscribed_channels"
    )

    date = models.DateTimeField(auto_now_add=True)
    objects = ChannelSubscriberManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["channel", "user"],
                name="unique_channel_subscribers"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} subscribed to {self.channel}"

    @classmethod
    def get_subscribers_count(cls, channel: Channel) -> int:
        """
        Return number of subscribers for a channel.
        """
        # Check the cache if subscriber count is already cached
        key = f'subscribers_count_{channel.token}'
        cached_subscribers_count = cache.get(key)

        if cached_subscribers_count is None:
            # If not cached, get count of subscribers from cache and db
            cached_subscribers_count = cls.__cached_subscribers_count(channel)
            db_subscribers_count = cls.__db_subscribers_count(channel)
            total_subscribers_count = cached_subscribers_count + db_subscribers_count
            # Set the count in cache
            cache.set(key, {'count': total_subscribers_count}, 60)
            return cached_subscribers_count + db_subscribers_count

        return cached_subscribers_count.get('count')

    @classmethod
    def __cached_subscribers_count(cls, channel: Channel) -> int:
        """
        Return number of subscribers which are only saved in cache
        args:
            channel: Channel
        """
        # Check the cache if subscriber count is already cached
        key = f"cache_subscriber_count_{channel.token}"
        cached_subscribers_count = cache.get(key)

        if cached_subscribers_count is None:
            # If not cached, get all subscribers from cache
            subscriber_key = f"subscriber:{channel.token}:*"
            cached_subscribers = [
                cache.get(key) for key in cache.keys(subscriber_key)
            ]
            # Filter out only subscribed which are in cache and not db
            subscriber_source_cache = filter(
                lambda subscriber: (
                   subscriber.get('subscription_status') == 'subscribed' and
                   subscriber.get('source') == 'cache'
                ),
                cached_subscribers
            )
            total_subscribers_count = len(list(subscriber_source_cache))
            # Set the count in cache
            cache.set(key, {'count': total_subscribers_count}, 60)
            return total_subscribers_count

        # If cached_channel_subscribers is not None
        return cached_subscribers_count.get('count')

    @classmethod
    def __db_subscribers_count(cls, channel: Channel) -> int:
        """
        Return number of subscribers which are only saved in db.
        args:
            channel: Channel
        """
        # Check the cache if subscriber count is already cached
        key = f"db_subscriber_count_{channel.token}"
        cached_db_subscribers_count = cache.get(key)

        if not cached_db_subscribers_count:
            # If not cached, get count of subscribers from db
            cached_db_subscribers_count = cls.objects.filter(
                channel=channel
            ).count()
            # Set the count in cache
            cache.set(key, {'count': cached_db_subscribers_count}, 60)
            return cached_db_subscribers_count

        # If cached_db_subscribers_count is not None
        return cached_db_subscribers_count.get('count')
