from django.db import models
from uuid import uuid4


class AbstractToken(models.Model):
    """
    An abstract model which provides a token field and auto fill it.
    """
    token = models.UUIDField(default=uuid4, unique=True, editable=False)

    class Meta:
        abstract = True
