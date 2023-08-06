class MembershipInUserError(Exception):
    """
    Exception raised when a membership is in use and tempted to be deleted.
    """
    pass
