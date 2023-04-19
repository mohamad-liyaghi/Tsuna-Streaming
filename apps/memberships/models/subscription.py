from django.db import models
from django.conf import settings
from django.utils import timezone
from memberships.models import Membership
import datetime
from core.models import BaseTokenModel


class Subscription(BaseTokenModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name="subscription")

    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name='subscriptions')
    
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name="unique_subscription"
            )
        ]


    def save(self, *args, **kwargs ):
        '''Change user status after creating a subscription'''

        if not self.pk:

            # If this is a new subscription, change the user's role to 'p' (Premium)
            if not self.user.role == 'a':
                self.user.role = 'p'
                self.user.save()

            # Get the Membership's active months
            membership_active_months = self.membership.active_months

            # Calculate the time that the subscription should expire
            finish_date = timezone.now() + datetime.timedelta(membership_active_months * 30)

            # set the expiration time
            self.finish_date = finish_date

        return super(Subscription, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        '''Change user status after deleting a subscription'''
        
        # When a subscription is deleted, change the user's role back to 'n' (normal)
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
    

