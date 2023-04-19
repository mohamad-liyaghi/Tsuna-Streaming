from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from votes.managers import VoteManager

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

    objects = VoteManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'object_id', 'user'],
                name="unique_vote"
            )
        ]

    def save(self, *args, **kwargs):

        if not self.pk:
            # the voted object
            object = self.content_object   

            # check if user voted before
            user_vote = object.votes.filter(user=self.user).first()

            if not user_vote:
                '''If user hasnt voted yet, vote object will be saved.'''

                return super(Vote, self).save(*args, **kwargs)


            if user_vote.choice == self.choice:
                '''Delete the vote if user sent 2 same values'''

                user_vote.delete()
                return None
            

            if user_vote.choice != self.choice:
                '''Update a vote if the given choice is diffrent from old choice'''
                
                user_vote.delete()
                return super(Vote, self).save(*args, **kwargs)
            
        return super(Vote, self).save(*args, **kwargs)
        


    def __str__(self) -> str:
        return str(self.user)