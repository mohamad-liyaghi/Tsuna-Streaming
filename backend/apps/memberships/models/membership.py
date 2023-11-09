from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from memberships.exceptions import MembershipInUserError
from core.models import AbstractToken


class Membership(AbstractToken):
    """
    Membership model is used to store the membership plans.
    """

    title = models.CharField(max_length=210)
    description = models.TextField(max_length=400, default="No Description available")

    price = models.PositiveBigIntegerField(
        default=10, validators=[MaxValueValidator(1000), MinValueValidator(10)]
    )

    active_months = models.PositiveBigIntegerField(
        default=0, validators=[MaxValueValidator(24), MinValueValidator(1)]
    )

    is_available = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    def delete(self, *args, **kwargs):
        """
        Only memberships without active subscription can be deleted
        """

        # Check membership is in use
        self.__check_in_use()
        return super(Membership, self).delete(*args, **kwargs)

    def __check_in_use(self) -> None:
        """
        Raise MembershipInUserError if trying to delete an in use plan
        """
        if self.subscriptions.count():
            raise MembershipInUserError("Plan is in use")
