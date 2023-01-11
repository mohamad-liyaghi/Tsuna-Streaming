from django.db import models
from v1.accounts.utils import token_generator


class Plan(models.Model):
    '''Subscription plan model'''

    title = models.CharField(max_length=210)
    description = models.TextField(max_length=400)

    price = models.PositiveBigIntegerField(default=0)
    
    token = models.CharField(max_length=32, default=token_generator)
    active_months = models.PositiveBigIntegerField(default=0)
    
    is_avaiable = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.token