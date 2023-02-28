class AdminNotFound(Exception):
    '''Raise when admin of a channel didnt found.'''
    pass

class ObjectPermissionDenied(Exception):
    '''Raise when user dont have add_object for that model'''
    pass
