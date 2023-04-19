from votes.tasks import remove_object_votes


def delete_object_votes_after_deleting(sender, instance, *args, **kwargs):
    '''Delete an objects votes that has been saved in db.'''

    # use celery to delete object votes
    remove_object_votes.delay(instance.get_model_content_type_id(), instance.id)