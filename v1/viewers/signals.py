from viewers.tasks import remove_object_viewers


def delete_object_viewers_after_deleting(sender, instance, *args, **kwargs):
    '''Delete an objects viewers that has been saved in db.'''
    
    remove_object_viewers.delay(instance.get_model_content_type_id, instance.id)