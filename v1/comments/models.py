from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from votes.models import Vote


class Comment(models.Model):
    '''Generic comment model'''

    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="replies")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')

    body = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)

    edited = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)

    token = models.CharField(max_length=32, null=True, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    vote = GenericRelation(Vote)

    def __str__(self) -> str:
        return str(self.user)