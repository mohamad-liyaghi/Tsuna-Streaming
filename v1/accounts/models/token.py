from django.db import models
from django.conf import settings
import datetime
from django.utils import timezone

from v1.accounts.utils import token_generator

class Token(models.Model):
    '''
        A 32 char token for email verification stuff.
        Token is valid for 10 mins and only can be tried for 5 times.
    '''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name="tokens")

    token = models.CharField(max_length=32, default=token_generator)
    date_created = models.DateTimeField(auto_now_add=True)
    retry = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return str(self.user)
    
    @property
    def is_valid(self):
        # check if tries are not more than 5 times.
        if self.retry == 5:
            return False
    
        # check if code was created within 10 mins
        now = timezone.now()
        ten_mins_before_now = now - datetime.timedelta(minutes=10)

        if self.date_created <=  ten_mins_before_now:
            return False

        return True

    
