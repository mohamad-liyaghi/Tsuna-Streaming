from django.db import models
from django.core.cache import cache
from django.conf import settings
from typing import Union
from datetime import datetime
from decouple import config
from channels.models import Channel
from channel_subscribers.utils import SubscriberStatus, SubscriberSource

# COMMON CACHE KEYS
CACHE_SUBSCRIBER_KEY = config('CACHE_CHANNEL_SUBSCRIBER')
CACHE_SUBSCRIBERS_COUNT_KEY = config('CACHE_CHANNEL_SUBSCRIBERS_COUNT')
CACHE_UNSUBSCRIBER_COUNT_KEY = config('CACHE_CHANNEL_UNSUBSCRIBER_COUNT')
CACHE_DB_SUBSCRIBERS_COUNT_KEY = config('CACHE_CHANNEL_DB_SUBSCRIBERS_COUNT')


class ChannelSubscriberManager(models.Manager):

    def get_count(self, channel: Channel) -> int:
        """
        Return number of subscribers for a channel.
        args:
            channel: Channel
        """

        key = CACHE_SUBSCRIBERS_COUNT_KEY.format(channel.token)
        # Get Check the cache to see if subscriber count is already cached
        cached_subscribers_count = cache.get(key)

        if cached_subscribers_count is None:
            # If not cached, get count of subscribers from cache and db
            cached_subscribers_count = self.__cached_subscribers_count(channel)
            db_subscribers_count = self.__db_subscribers_count(channel)
            # Get count of unsubscribed subscribers from cache
            # which their records are in db
            ubsubscribed_count = self.__cached_unsubscribed_count(channel)

            # Calculate total subscriber count
            total_subscriber_count = (
                cached_subscribers_count +
                (db_subscribers_count - ubsubscribed_count)
            )

            # Set the count in cache
            cache.set(key, {'count': total_subscriber_count}, 60)
            return total_subscriber_count

        return cached_subscribers_count.get('count')

    def get_list(self, channel: Channel) -> dict:
        subscriber_key = CACHE_SUBSCRIBER_KEY.format(channel.token, '*')

        cache_subscribers = [
            cache.get(key) for key in cache.keys(subscriber_key)
        ]

        db_subscribers = list(
            self.model.objects.filter(channel=channel)
        )
        # Filter out only subscribed which are in cache and not db
        cache_subscribers = list(
            filter(
                lambda subscriber: (
                        subscriber.get('subscription_status') == SubscriberStatus.SUBSCRIBED.value
                        and
                        subscriber.get('source') == SubscriberSource.CACHE.value
                ),
                cache_subscribers
            )
        )
        return cache_subscribers + db_subscribers

    def get_from_cache(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL
    ) -> Union[dict, None]:
        """
        Get subscriber from cache/db and return it.
        args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
        """
        # Check if subscriber exists in db
        subscriber_in_db = self.__get_from_db(channel, user)
        # Check if subscriber exists in cache
        subscriber_in_cache = self.__get_from_cache(channel, user)

        # If subscriber is in DB, return it
        if subscriber_in_db:
            return subscriber_in_db

        # If there is a subscriber in cache
        if subscriber_in_cache:
            # If the subscriber is subscribed, return True
            if subscriber_in_cache.get('subscription_status') == SubscriberStatus.SUBSCRIBED.value:
                return subscriber_in_cache
            # If the subscriber is unsubscribed, return None
            return

        return

    def create_in_cache(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL
    ) -> Union[dict, None]:
        """
        Create a subscriber in cache
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
        """

        # Check if subscriber already exists in cache or db
        # If subscriber exists, return None
        if self.get_from_cache(channel, user):
            return

        # If not exist, create a new subscriber in cache
        return self.__set_cache(
            channel=channel,
            user=user,
            subscription_status=SubscriberStatus.SUBSCRIBED.value,
        )

    def delete_in_cache(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL
    ) -> None:
        """
        Delete a subscriber from cache
        If subscriber is in db, create a record in cache with
        subscription_status = unsubscribed
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
        """

        # Check if subscriber already exists in cache or db
        cached_subscriber = self.get_from_cache(channel, user)

        # If not exist, raise error
        if not cached_subscriber:
            raise ValueError("Subscriber does not exist in cache")

        # If source is database, update its status to unsubscribed
        # So then celery task can delete it from db
        if cached_subscriber.get('source') == SubscriberSource.DATABASE.value:
            self.__set_cache(
                channel=channel,
                user=user,
                subscription_status=SubscriberStatus.UNSUBSCRIBED.value,
                source=SubscriberSource.DATABASE.value
            )
            return

        # If source is in cache, remove the record
        key = CACHE_SUBSCRIBER_KEY.format(channel.token, user.token)
        cache.delete(key)
        return

    def __cached_subscribers_count(self, channel: Channel) -> int:
        """
        Return number of subscribers which are only saved in cache
        args:
            channel: Channel
        """
        # Check the cache if subscriber count is already cached
        key =  CACHE_SUBSCRIBERS_COUNT_KEY.format(channel.token)
        cached_subscribers_count = cache.get(key)

        if cached_subscribers_count is None:
            # If not cached, get all subscribers from cache
            subscriber_key = CACHE_SUBSCRIBER_KEY.format(channel.token, '*')
            cached_subscribers = [
                cache.get(key) for key in cache.keys(subscriber_key)
            ]
            # Filter out only subscribed which are in cache and not db
            subscriber_source_cache = filter(
                lambda subscriber: (
                        subscriber.get('subscription_status') == SubscriberStatus.SUBSCRIBED.value
                        and
                        subscriber.get('source') == SubscriberSource.CACHE.value
                ),
                cached_subscribers
            )

            total_subscribers_count = len(list(subscriber_source_cache))
            # Set the count in cache
            cache.set(key, {'count': total_subscribers_count}, 60)
            return total_subscribers_count

        # If cached_channel_subscribers is not None
        return cached_subscribers_count.get('count')

    def __db_subscribers_count(self, channel: Channel) -> int:
        """
        Return number of subscribers which are only saved in db.
        args:
            channel: Channel
        """
        # Check the cache if subscriber count is already cached
        key = CACHE_DB_SUBSCRIBERS_COUNT_KEY.format(channel.token)
        cached_db_subscribers_count = cache.get(key)

        if not cached_db_subscribers_count:
            # If not cached, get count of subscribers from db
            cached_db_subscribers_count = self.model.objects.filter(
                channel=channel
            ).count()
            # Set the count in cache
            cache.set(key, {'count': cached_db_subscribers_count}, 60)
            return cached_db_subscribers_count

        # If cached_db_subscribers_count is not None
        return cached_db_subscribers_count.get('count')

    def __cached_unsubscribed_count(self, channel: Channel) -> int:
        """
        Return number of unsubscribed records which are only saved in cache
        args:
            channel: Channel
        """
        # Check the cache if subscriber count is already cached
        key = CACHE_UNSUBSCRIBER_COUNT_KEY.format(channel.token)
        cached_count = cache.get(key)

        if cached_count is None:
            # If not cached, get all subscribers from cache
            subscriber_key = CACHE_SUBSCRIBER_KEY.format(channel.token, '*')
            cached_subscribers = [
                cache.get(key) for key in cache.keys(subscriber_key)
            ]

            # Filter only subscribers with subscription_status = unsubscribed
            filter_unsubscribed = filter(
                lambda subscriber: (
                        subscriber.get('source') == SubscriberSource.DATABASE.value and
                        subscriber.get('subscription_status') == SubscriberStatus.UNSUBSCRIBED.value
                ),
                cached_subscribers
            )

            total_unsubscribed = len(list(filter_unsubscribed))
            # Set the count in cache
            cache.set(key, {'count': total_unsubscribed}, 60)
            return total_unsubscribed

        # If cached_channel_subscribers is not None
        return cached_count.get('count', 0)

    def __get_from_cache(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL
    ) -> Union[dict, None]:
        """
        Get subscriber from cache and return it.
        if not exist, return None
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
        """
        key = CACHE_SUBSCRIBER_KEY.format(channel.token, user.token)
        # Get subscriber from cache
        cache_subscriber = cache.get(key)

        if cache_subscriber is not None:
            return cache_subscriber

        return

    def __get_from_db(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL
    ) -> Union[dict, None]:
        """
        Get subscriber from database and return it.
        if not exist, return False
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
        """
        # Get from cache first
        key = CACHE_SUBSCRIBER_KEY.format(channel.token, user.token)
        db_subscriber = cache.get(key)

        if not db_subscriber:
            # Check if subscriber exists in db
            subscriber = self.model.objects.filter(
                user=user,
                channel=channel
            )
            # Set subscriber in cache and return it
            if subscriber.exists():
                return self.__set_cache(
                    channel=channel,
                    user=user,
                    subscription_status=SubscriberStatus.SUBSCRIBED.value,
                    source=SubscriberSource.DATABASE.value
                )

            # Return none if subscriber does not exist in db
            return

        return db_subscriber

    def __set_cache(
            self,
            channel: Channel,
            user: settings.AUTH_USER_MODEL,
            subscription_status: str = SubscriberStatus.SUBSCRIBED.value,
            source: str = SubscriberSource.CACHE.value,
            date: datetime =datetime.now()
    ) -> dict:
        """
        Set subscriber in cache
        Args:
            channel: Channel
            user: settings.AUTH_USER_MODEL
            subscription_status: str
            source: str
        """
        key = CACHE_SUBSCRIBER_KEY.format(channel.token, user.token)

        cache.set(
            key=key,
            value={
                'user': user,
                'channel': channel,
                'subscription_status': subscription_status,
                'source': source,
                'date': date
            },
            timeout=60
        )
        return cache.get(key)
