from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Vote(models.Model):
    '''Generic vote model'''

    class Choice(models.TextChoices):
        UPVOTE = ("u", "Upvote")
        DOWNVOTE = ("d", "Downvote")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes")
    choice = models.CharField(max_length=1, choices=Choice.choices, default=Choice.UPVOTE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id', 'user'],
                name="unique_vote"
            )
        ]

    def __str__(self) -> str:
        return str(self.user)