from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from votes.models import Vote
from comments.exceptions import CommentNotAllowed
from core.models import BaseTokenModel


class Comment(BaseTokenModel):
    '''Generic comment model'''

    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="replies")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')

    body = models.TextField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)

    edited = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    votes = GenericRelation(Vote)

    def save(self, *args, **kwargs):
    
        if not self.pk:
            # if object dont allow adding comment, an error will be raised.
            if not self.content_object.allow_comment:
                raise CommentNotAllowed("Comments are closed")

        # if object has pk it means that it is getting updated.
        self.edited = True
        return super(Comment, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.user)