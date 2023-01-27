from django.db import models


class VideoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def published(self):
        return self.get_queryset().filter(visibility="pu")