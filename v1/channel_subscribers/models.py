from django.db import models
from django.utils import timezone
from django.core.cache import cache
from channels.models import Channel
from accounts.models import Account


class ChannelSubscriber(models.Model):
    """Model to represent a user's subscription to a channel."""
    
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="subscribers")
    user = models.ForeignKey(Account, on_delete=models.CASCADE,
                             related_name="subscribed_channels")

    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["channel", "user"],
                name="unique_channel_subscribers"
            )
        ]

    def __str__(self) -> str:
        return str(self.user)
    

    @classmethod
    def get_subscriber(cls, channel_token, user_token):
        '''Get subscriber from cache and return it. if not exist in cache, get from database.'''

        key = f'subscriber:{channel_token}:{user_token}'
        # Get subscriber from cache
        cache_subscriber = cache.get(key)

        # if Subscriber exists in cache
        if cache_subscriber:
            # If status of the subscriber in cache is subscribed means user has subscribed
            # If status of subscriber is unsubscribed, means user has unsubscribed
            if cache_subscriber.get('subscription_status', None) == 'subscribed':
                return cache_subscriber
            
            return None
        
        # if subscriber is not in cache
        else:  
                # Get subscriber from database
                subscriber = cls.objects.filter(user__token=user_token, channel__token=channel_token).exists()
                # if subscriber exists in cache
                if subscriber:
                    # set subscriber in cache
                    cache.set(
                        key=key, 
                        value={
                            'subscription_status' : 'subscribed', 
                            'source' : 'database'
                        },
                        timeout=60 * 60 * 24)
                    
                    # return subscriber
                    return cache.get(key)
                
                return None
        

    @classmethod
    def create_subscriber(cls, channel_token, user_token):
        '''
            If user has subscribed a channel, it sets in cache and return None
            otherwise it sets the subscription in cache and return the info
        '''
        
        key = f'subscriber:{channel_token}:{user_token}'

        # Get the user from cache
        cache_subscriber = cache.get(key)

        # If user exists in cache
        if cache_subscriber:

            # If subscription_status == 'ubsubscribed' means that user has unsubscribed and not wants to subscribe again
            if cache_subscriber.get('subscription_status', None) == 'unsubscribed':
                    cache.set(
                    key=key,
                    value={
                        'subscription_status': 'subscribed',
                        'source': 'cache',
                        'date' : timezone.now(),
                    },
                    timeout=60 * 60 * 24)
                    return cache.get(key)
            
            # If user is in cache and already subscribed the channel, it returns None
            return None
            

            
        # If subscriber is not in cache and it is in db it sets the user in cache and return None
        # Cuz user has Subscribed the channel
        elif cls.objects.filter(user__token=user_token, channel__token=channel_token).exists():

            # Set the subscriber in cache for subsequent requests
            cache.set(
                key=key,
                value={
                    'subscription_status': 'subscribed',
                    'source': 'database'
                },
                timeout=60 * 60 * 24
            )

            return None

        # If subscriber not exists in cache and also in DB
        # It sets the subscriber in cache and after that celery inserts them into db
        else:
            user = Account.objects.filter(token=user_token).exists()
            channel = Channel.objects.filter(token=channel_token).exists()
            # If user and channel are valid set a cache
            if user and channel:
                cache.set(
                    key=key,
                    value={
                        'subscription_status' : 'subscribed', 
                        'source' : 'cache'
                    }, 
                    timeout=60 * 60 * 24
                    )
                return cache.get(key)
            
            return None

    
    @classmethod
    def delete_subscriber(cls, channel_token, user_token):
        key = f'subscriber:{channel_token}:{user_token}'

        # Get the subscriber from the cache
        cache_subscriber = cache.get(key)

        # If subscriber is in cache
        if cache_subscriber:

            # If user has already subscribed the channel and exists in cache
            # It will update the cache that user has unsubscribed
            # Then celery will delete the sub
            if cache_subscriber.get('subscription_status', None) == 'subscribed':
                
                # Update the cache
                cache.set(
                key=key,
                value={
                    'subscription_status' : 'unsubscribed', 
                    'source' : 'cache'
                }, 
                timeout=60 * 60 * 24
                )
                return cache.get(key)
            
            # if subscription_status is unsubscribed
            return None
        
        # If sub is not in cache but in db
        elif cls.objects.filter(user__token=user_token, channel__token=channel_token).exists():
            
            # Set a cache that user has unsubscribed
            cache.set(
                key=key,
                value={
                    'subscription_status': 'unsubscribed',
                    'source': 'cache'
                },
                timeout=60 * 60 * 24
            )

            return cache.get(key)
        
        # If not in cache not in db it returns None
        return None