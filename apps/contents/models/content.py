from django.db import models
from django.core.exceptions import PermissionDenied
from django.contrib.contenttypes.fields import GenericRelation

from core.models import AbstractToken
from .utils import (
    get_thumbnail_upload_path,
    get_file_upload_path
)
from core.utils import get_content_type_model
from .visibility import ContentVisibility


class AbstractContent(AbstractToken):
    """
    Abstract model for content models
    Provide the common fields for content models
    """

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)

    # The actual file of the content
    file = models.FileField(upload_to=get_file_upload_path)

    # The thumbnail of the content
    thumbnail = models.ImageField(
        upload_to=get_thumbnail_upload_path,
        default="assets/images/default-thumbnail.jpg"
    )

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
        """
        Return content model by name
        """

        for subclass in cls.__subclasses__():
            if subclass.__name__ == name:
                return subclass

        return None

    def save(self, *args, **kwargs):
        if self.pk:
            # update is_updated field if an object is updated
            self.is_updated = True

        if not self.pk:
            # Check user is admin and has permission to add object
            self.__check_admin_permission(
                user=self.user, channel=self.channel
            )

        return super(AbstractContent, self).save(*args, **kwargs)

    def __check_admin_permission(self, user, channel) -> bool:
        """Check if user has permission to add object"""
        admin = user.channel_admins.filter(channel=channel).first()
        if not admin:
            raise PermissionDenied("Admin didnt found.")

        if not admin and admin.permissions.filter(
                model=get_content_type_model(model=self.__class__),
                add_object=True
        ).exists():
            raise PermissionDenied("Admin dont have permission to add object.")

        # Return True if user is admin and has add_object permission
        return True
