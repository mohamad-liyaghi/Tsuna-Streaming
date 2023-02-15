from django.db.models.signals import pre_save
from comments.models import Comment
from config.receivers import create_token_after_creating_object

# create token for each comment
pre_save.connect(create_token_after_creating_object, sender=Comment)

def delete_object_comments_after_deleting(sender, instance, *args, **kwargs):
    '''Delete an objects comments that has been saved in db.'''
    
    instance.comment.all().delete()