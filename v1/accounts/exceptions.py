class PlanInUseError(Exception):
    '''Raise this when a plan that has active subs is going to be deletd.'''
    pass