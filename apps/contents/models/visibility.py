from django.db import models

class ContentVisibility(models.TextChoices):
    """
    Content visibility choices
    """
    PRIVATE = ("pr", "Private")
    PUBLISHED = ("pu", "Public")
