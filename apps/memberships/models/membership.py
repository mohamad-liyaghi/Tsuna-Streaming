from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from memberships.exceptions import MembershipInUserError
from core.models import BaseTokenModel


class Membership(BaseTokenModel):
    '''Membership plans for users to buy'''

    title = models.CharField(max_length=210)
    description = models.TextField(max_length=400, default="No Description available")

    price = models.PositiveBigIntegerField(default=10, validators=[
        MaxValueValidator(1000),
        MinValueValidator(10)
    ])


    active_months = models.PositiveBigIntegerField(default=0,validators=[
        MaxValueValidator(24),
        MinValueValidator(1)
    ])

    is_available = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.title

    def delete(self, *args, **kwargs):
        '''User cannot delete the plan if there are subscriptions for target plan.'''

        if (sub_counts:=self.subscriptions.count()):
            raise MembershipInUserError(f"Plan is already in use by {sub_counts} users")
        
        return super(Membership, self).delete(*args, **kwargs)

