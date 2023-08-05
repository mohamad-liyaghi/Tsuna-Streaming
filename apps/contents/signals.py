from django.db.models.signals import post_save, post_delete
from contents.models import AbstractContent
from votes.signals import delete_vote_after_deleting_object
from comments.signals import delete_object_comments_after_deleting
from viewers.signals import delete_object_viewers_after_deleting


# Delete votes, comments, viewers after deleting a sub object of AbstractContent
post_delete.connect(delete_vote_after_deleting_object, sender=AbstractContent)
post_delete.connect(delete_object_comments_after_deleting, sender=AbstractContent)
post_delete.connect(delete_object_viewers_after_deleting, sender=AbstractContent)
