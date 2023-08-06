from django.db import models


class SubscriptionManager(models.Manager):
    """
    Custom manager for the Subscription model.
    """
    def get_active_subscription(self, user: 'Account'):
        """
        Returns the active subscription for the given user.
        """
        subscription = self.filter(user=user).first()
        if subscription and subscription.is_active:
            return subscription
        return
