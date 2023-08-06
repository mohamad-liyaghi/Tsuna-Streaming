from rest_framework.throttling import UserRateThrottle


class VideoThrottle(UserRateThrottle):
    """
    Custom throttle for video views.
    """
    scope = 'video'
