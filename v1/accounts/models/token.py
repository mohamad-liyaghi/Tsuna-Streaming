from django.db import models
from django.conf import settings

class Token(models.Model):
    '''
        A 32 char token for email verification stuff.
        Token is valid for 10 mins and only can be tried for 5 times.
    '''

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name="tokens")

    token = models.CharField(max_length=32)
    date_created = models.DateTimeField(auto_now_add=True)
    retry = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.user
    
