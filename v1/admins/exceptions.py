class AdminAlreadyExists(Exception):
    '''Raise this exception when an admin is getting promoted twice.'''
    pass

class AdminNotSubscribed(Exception):
    '''Raise this exception when promoting a user that hasnt subscribed the channel.'''
    pass

