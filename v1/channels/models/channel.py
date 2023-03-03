from django.db import models
from django.conf import settings
from accounts.validators import validate_profile_size
from channels.exceptions import ChannelLimitException


class Channel(models.Model):
    
    title = models.CharField(max_length=240)
    description = models.TextField(max_length=500, default="A new channel on Tsuna Streaming.")

    profile = models.ImageField(upload_to="channels/profile", default="assets/images/default-channel-profile.jpg",
                                    validators=[validate_profile_size,])

    thumbnail = models.ImageField(upload_to="channels/profile", default="assets/images/default-thumbnail.jpg",
                                    validators=[validate_profile_size,])
    
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                related_name="channels")

    token = models.CharField(max_length=32, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)

    @property
    def subscribers_count(self):
        return self.subscribers.all().count()

    @property
    def videos_count(self):
        return self.videos.all().count()

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
                
                raise ChannelLimitException("User has reached maximum number of channels to create.")

            # normal users can create less than 5 channels
            # normal users that had premium sub and created more that 5 channels, now can create less that 10 channels.
            elif self.owner.role == 'n':

                # normal users that hadnt premiums account yet.
                if user_channels < 5:
                    return super(Channel, self).save(*args, **kwargs)
            
                # for normal users that have had premium accounts and created over 5 channels.
                elif user_channels > 6 and user_channels < 10:
                    return super(Channel, self).save(*args, **kwargs)
                
                raise ChannelLimitException("User has reached maximum number of channels to create.")
                
            return super(Channel, self).save(*args, **kwargs)

        return super(Channel, self).save(*args, **kwargs)
    

    def __str__(self) -> str:
        return self.title