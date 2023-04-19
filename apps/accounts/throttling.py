from rest_framework.throttling import AnonRateThrottle

class AuthenticationThrottle(AnonRateThrottle):
    '''Throttling for Register/Verify/Login views'''
    
    scope = "authentication"

