def delete_object_viewers_after_deleting(sender, instance, *args, **kwargs):
    '''Delete an objects viewers that has been saved in db.'''
    
    instance.viewer.all().delete()