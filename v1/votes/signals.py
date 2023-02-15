def delete_object_votes_after_deleting(sender, instance, *args, **kwargs):
    '''Delete an objects votes that has been saved in db.'''
    
    instance.vote.all().delete()