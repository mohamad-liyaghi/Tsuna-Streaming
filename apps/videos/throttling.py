from rest_framework.throttling import UserRateThrottle


class VideoThrottle(UserRateThrottle):
    '''Custom throttle for video list/detail/create page.'''
    scope = 'video'