from comments.tasks import remove_object_comments


def delete_object_comments_after_deleting(sender, instance, *args, **kwargs):
    '''Delete an objects comments that has been saved in db.'''
    
    remove_object_comments.delay(instance.get_model_content_type_id(), instance.id)