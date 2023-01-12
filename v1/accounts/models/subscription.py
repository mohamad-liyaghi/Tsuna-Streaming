from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from v1.accounts.utils import token_generator


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