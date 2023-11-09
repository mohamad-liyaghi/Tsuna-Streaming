from django.db import models
from contents.models.visibility import ContentVisibility


class BaseContentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def published(self):
        """
        Return only published contents.
        """
        return self.get_queryset().filter(visibility=ContentVisibility.PUBLISHED)
