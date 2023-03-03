from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from accounts.exceptions import PlanInUseError


class Plan(models.Model):
    '''Subscription plan model'''

    title = models.CharField(max_length=210)
    description = models.TextField(max_length=400, default="No Description available")

    price = models.PositiveBigIntegerField(default=10, validators=[
        MaxValueValidator(1000),
        MinValueValidator(10)
    ])
    
    token = models.CharField(max_length=32, null=True, blank=True)

    active_months = models.PositiveBigIntegerField(default=0,validators=[
        MaxValueValidator(24),
        MinValueValidator(1)
    ])

    is_available = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        '''User cannot delete the plan if there are subscriptions for target plan.'''

        if (sub_counts:=self.plans.count()):
            raise PlanInUseError("Plan is already in use by {} users".format(sub_counts))
        
        return super(Subscription, self).delete(*args, **kwargs)


    def __str__(self) -> str:
        return self.title


class Subscription(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name="subscriptions")

    plan = models.ForeignKey("Plan", on_delete=models.CASCADE, related_name='plans')
    
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)

    token = models.CharField(max_length=32, null=True, blank=True)

    def save(self, *args, **kwargs ):

        if not self.pk:
            if not self.user.role == 'a':
                self.user.role = 'p'
                self.user.save()

        return super(Subscription, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        '''Change user status after deleting a subscription'''
        
        if not self.user.role == 'a':
            self.user.role = 'n'
            self.user.save()

        return super(Subscription, self).delete(*args, **kwargs)

    @property
    def is_active(self):     
        now = timezone.now()  

        if now <= self.finish_date:
            return True

        return False

    def __str__(self) -> str:
        return str(self.token)


