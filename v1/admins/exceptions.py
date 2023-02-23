class AdminExistsError(Exception):
    '''Raise this exception when an admin is getting promoted twice.'''
    pass

class AdminNotSubscribedError(Exception):
    '''Raise this exception when promoting a user that hasnt subscribed the channel.'''
    pass

class PromotePermissionDenied(Exception):
    '''Raise this error when user do not have permission to promote admin'''
    pass

