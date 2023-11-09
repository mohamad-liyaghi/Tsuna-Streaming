from django.db import models
from memberships.models import Subscription


class AbstractAccountRole(models.Model):
    """
    Account roles
    Methods:
        is_admin)(: Check if user is admin
        is_premium(): Check if user is premium (has an active subscription)
        is_normal(): Check if user is normal
    """

    class Meta:
        abstract = True

    def is_admin(self) -> bool:
        """Check if user is admin"""
        return self.is_superuser

    def is_premium(self) -> bool:
        """Check if user has an active subscription"""
        return bool(Subscription.objects.get_active_subscription(user=self))

    def is_normal(self) -> bool:
        """Check to see user is not admin and not premium"""
        return not (self.is_admin() or self.is_premium())
