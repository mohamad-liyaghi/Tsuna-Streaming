from django.db import models
from django.conf import settings
from django.core.cache import cache
from accounts.validators import validate_profile_size
from channels.exceptions import ChannelLimitExceededException
from core.models import BaseTokenModel


class Channel(BaseTokenModel):
    
    title = models.CharField(max_length=240)
    description = models.TextField(max_length=500, default="A new channel on Tsuna Streaming.")

    profile = models.ImageField(upload_to="channels/profile", default="assets/images/default-channel-profile.jpg",
                                    validators=[validate_profile_size,])

    thumbnail = models.ImageField(upload_to="channels/profile", default="assets/images/default-thumbnail.jpg",
                                    validators=[validate_profile_size,])
    
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                related_name="channels")

    date_joined = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)

    @property
    def subscribers_count(self):
        key = f'subscriber_count:{self.token}'
        cache_subscribers_count = cache.get(key)

        # If subscriber count in cache return that
        if cache_subscribers_count is not None:
            return cache_subscribers_count.get("count", 0)
            
        # If subscriber count not in cache
        # Get all subscribers from cache
        cached_subscribers = [cache.get(key) for key in cache.keys(f"subscriber:{self.token}:*")]
        
        # Get subscribers count from db
        db_subscribers_count = self.subscribers.count()

        # If there are subs in cache
        if cached_subscribers:   
            # Give len of subscribers that have subscription subscribed and source in cache 
            cached_subscriber_count = sum(
            1 for sub in cached_subscribers
            if sub.get('subscription_status') == 'subscribed' and sub.get('source') == 'cache')

            # Total of subscribers
            total_subscribers = db_subscribers_count + cached_subscriber_count
            # Set the count in cache for other requests
            cache.set(key=key, value={'count' : total_subscribers}, timeout=5 * 60)
            # Return total subs
            return total_subscribers

        # If no subscriber in cache, save the subs count of db in cache and return it
        cache.set(key=key, value={'count' : db_subscribers_count}, timeout=5 * 60)
        return db_subscribers_count


    def save(self, *args, **kwargs):
        
        if not self.pk:
            user_channels = self.owner.channels.count()

            # admin users can create unlimited amount of channel
            if self.owner.role == 'a':
                return super(Channel, self).save(*args, **kwargs)
            
            #  premium users can create less than 10 channels.
            elif self.owner.role ==  'p':
                # Premium user can only create 10 channels.
                if user_channels < 10:
                    return super(Channel, self).save(*args, **kwargs)
                
                raise ChannelLimitExceededException("User has reached maximum number of channels to create.")

            # normal users can create less than 5 channels
            # normal users that had premium sub and created more that 5 channels, now can create less that 10 channels.
            elif self.owner.role == 'n':

                # normal users that hadnt premiums account yet.
                if user_channels < 5:
                    return super(Channel, self).save(*args, **kwargs)
            
                # for normal users that have had premium accounts and created over 5 channels.
                elif user_channels > 6 and user_channels < 10:
                    return super(Channel, self).save(*args, **kwargs)
                
                raise ChannelLimitExceededException("User has reached maximum number of channels to create.")
                
            return super(Channel, self).save(*args, **kwargs)

        return super(Channel, self).save(*args, **kwargs)
    

    def __str__(self) -> str:
        return self.title