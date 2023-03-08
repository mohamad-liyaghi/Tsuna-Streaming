class DuplicatePromotionException(Exception):
    '''Raise this exception when an admin is getting promoted twice.'''
    pass


class SubscriptionRequiredException(Exception):
    '''Raise this exception when promoting a user that hasnt subscribed the channel.'''
    pass

