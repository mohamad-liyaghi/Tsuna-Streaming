from django.db import models


class VoteChoice(models.TextChoices):
    UPVOTE = ("u", "Upvote")
    DOWNVOTE = ("d", "Downvote")
