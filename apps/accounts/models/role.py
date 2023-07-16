from django.db import models


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
        # TODO: get_premium_plan
        """Check if user has an active subscription"""
        subscription = self.subscription.first()
        return (subscription and subscription.is_active)

    def is_normal(self) -> bool:
        """Check to see user is not admin and not premium"""
        return not (self.is_admin() or self.is_premium())
