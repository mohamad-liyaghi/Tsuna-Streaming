from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from v1.accounts.utils import token_generator
from accounts.managers import SubscriptionManager

class Plan(models.Model):
    '''Subscription plan model'''

    title = models.CharField(max_length=210)
    description = models.TextField(max_length=400, default="No Description available")

    price = models.PositiveBigIntegerField(default=10, validators=[
        MaxValueValidator(1000),
        MinValueValidator(10)
    ])
    
    token = models.CharField(max_length=32, default=token_generator)

    active_months = models.PositiveBigIntegerField(default=0,validators=[
        MaxValueValidator(24),
        MinValueValidator(1)
    ])

    is_available = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.token


class Subscription(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name="subscriptions")

    plan = models.ForeignKey("Plan", on_delete=models.CASCADE)
    
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)

    token = models.CharField(max_length=32, default=token_generator)    

    objects = SubscriptionManager()

    def __str__(self) -> str:
        return str(self.token)


