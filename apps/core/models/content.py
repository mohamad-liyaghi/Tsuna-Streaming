from django.db import models
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.fields import GenericRelation

from django.core.cache import cache
from .token import AbstractToken
from core.utils import get_content_type_model


class ContentVisibility(models.TextChoices):
    """
    Content visibility choices
    """
    PRIVATE = ("pr", "Private")
    PUBLISHED = ("pu", "Public")


class AbstractContent(AbstractToken):
    """
    Abstract model for content models
    Provide the common fields for content models
    """
    # TODO: update fields
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)

    visibility = models.CharField(
        max_length=2,
        choices=ContentVisibility.choices,
        default=ContentVisibility.PRIVATE
    )
    is_updated = models.BooleanField(default=False)

    # whether or not user can add comment
    allow_comment = models.BooleanField(default=True)

    date = models.DateTimeField(auto_now_add=True)

    votes = GenericRelation('votes.Vote')
    comments = GenericRelation('comments.Comment')
    viewers = GenericRelation('viewers.Viewer')

    class Meta:
        abstract = True

    @property
    def is_published(self):
        """Return True if object is status is PUBLISHED"""
        return self.visibility == ContentVisibility.PUBLISHED

    @classmethod
    def get_content_model_by_name(cls, name):
        # TODO: remove this
        '''Return the subclass content model'''

        for subclass in cls.__subclasses__():
            if subclass.__name__ == name:
                return subclass

        return None

    def get_viewer_count(self):
        # TODO: Move this
        '''Return objects viewers count'''
        # get object viewer count from cache
        db_viewers_count = cache.get(f'db_viewer_count:{self.token}')

        # if cache not exist, calculate from db
        if not db_viewers_count:
            db_viewers_count = self.viewers.count()
            # set viewers count in cache
            cache.set(f'db_viewer_count:{self.token}', db_viewers_count, timeout=10 * 60)

        viewers_in_cache = [
            cache.get(viewer) for viewer in cache.keys("viewer:*:*")
        ]

        # total of those caches with source == cache
        cache_viewers_count = sum(
            1
            for viewer in viewers_in_cache
            if viewer.get("source") == "cache"
        )

        return db_viewers_count + cache_viewers_count

    def get_votes_count(self):
        # TODO: Move this
        '''Get count of up/down votes of an object'''

        key = f"vote_count:{self.token}"
        cached_vote_count = cache.get(key)

        if cached_vote_count:
            # if votes count exists in cache
            return cached_vote_count

        # if not exist in cache
        votes_in_db = self.votes.all()
        upvotes_in_db = votes_in_db.filter(choice="u").count()
        downvotes_in_db = votes_in_db.filter(choice="d").count()

        votes_in_cache = [
            cache.get(vote) for vote in cache.keys(f"vote:{self.token}:*")
        ]

        upvotes_in_cache = sum(
            1
            for upvote in votes_in_cache
            if upvote.get("source") == "cache" and upvote.get("choice") == "u"
        )

        downvotes_in_cache = sum(
            1
            for downvote in votes_in_cache
            if downvote.get("source") == "cache" and downvote.get("choice") == "d"
        )

        # set votes count in cache
        cache.set(
            key,
            {
                "upvotes": upvotes_in_cache + upvotes_in_db,
                "downvotes": downvotes_in_cache + downvotes_in_db,
            },
            timeout=120,  # Use seconds instead of minutes
        )

        return cache.get(key)

    def save(self, *args, **kwargs):
        # TODO: update this
        if self.pk:
            # update is_updated field if an object is updated
            self.is_updated = True
            return super(AbstractContent, self).save(*args, **kwargs)

        if not self.pk:
            # get the object channels admin
            admin = self.user.channel_admins.filter(channel=self.channel).first()

            if admin:
                # check if user has permission
                if admin.permissions.filter(
                        model=get_content_type_model(model=self.__class__),
                        add_object=True
                ).exists():
                    return super(AbstractContent, self).save(*args, **kwargs)

                raise PermissionDenied("Admin dont have permission to add object.")

            raise PermissionDenied("Admin didnt found.")

        return super(AbstractContent, self).save(*args, **kwargs)


