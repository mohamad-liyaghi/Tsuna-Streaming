from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import PermissionDenied
import datetime
from memberships.models import Membership
from memberships.managers import SubscriptionManager
from core.models import AbstractToken


class Subscription(AbstractToken):
    """
    Subscription model is used to store the user's subscription.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    membership = models.ForeignKey(
        Membership,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)

    objects = SubscriptionManager()

    @property
    def is_active(self):
        """
        Check if the subscription is active
        """
        now = timezone.now()
        return self.end_date and now <= self.end_date

    class Meta:
        """
        Set unique constraint on user field
        """
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name="unique_subscription"
            )
        ]

    def save(self, *args, **kwargs):
        """
        Set the finish date if the subscription is new
        """

        if not self.pk:
            self.__check_user_role()
            self.__check_membership_is_available()
            self.__set_end_date()

        return super(Subscription, self).save(*args, **kwargs)

    def __set_end_date(self):
        membership_active_months = self.membership.active_months
        self.end_date = (
                timezone.now() + datetime.timedelta(membership_active_months * 30)
        )

    def __check_user_role(self):
        if not self.user.is_active:
            raise PermissionDenied("User is not active")

        if not self.user.is_normal():
            raise PermissionDenied("Only normal users can have a subscription")

    def __check_membership_is_available(self):
        """
        Check if the membership is available
        """
        if not self.membership.is_available:
            raise PermissionDenied("Membership is not available to subscribe")

    def __str__(self) -> str:
        return f"{self.user} - {self.membership}"
