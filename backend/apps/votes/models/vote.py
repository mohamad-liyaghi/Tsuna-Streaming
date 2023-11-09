from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from channels.models import Channel
from votes.managers import VoteManager
from core.models import AbstractToken
from .vote_choice import VoteChoice


class Vote(AbstractToken):
    """
    A generic model for votes
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes"
    )
    choice = models.CharField(
        max_length=1, choices=VoteChoice.choices, default=VoteChoice.UPVOTE
    )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = VoteManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["content_type", "object_id", "user"], name="unique_vote"
            )
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            # Set channel for the vote
            self.__set_channel()

        return super(Vote, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.user)

    def __set_channel(self) -> None:
        self.channel = self.content_object.channel
