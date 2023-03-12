from django.db import models
from django.conf import settings
from django.utils import timezone
from memberships.models import Membership


class Subscription(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name="subscription")

    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name='subscriptions')
    
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)

    token = models.CharField(max_length=32, null=True, blank=True)


    def save(self, *args, **kwargs ):
        '''Change user status after creating a subscription'''

        if not self.pk:

            if not self.user.role == 'a':
                self.user.role = 'p'
                self.user.save()

        return super(Subscription, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        '''Change user status after deleting a subscription'''
        
        if not self.user.role == 'a':
            self.user.role = 'n'
            self.user.save()

        return super(Subscription, self).delete(*args, **kwargs)


    @property
    def is_active(self):     
        '''Check if subscription is active'''
        now = timezone.now()  

        if self.finish_date and now <= self.finish_date:
            return True

        return False


    def __str__(self) -> str:
        return f"{self.user.email}"
    

