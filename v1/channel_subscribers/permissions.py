from rest_framework.permissions import BasePermission
from channel_subscribers.models import ChannelSubscriber


class SubscriberPermission(BasePermission):
    '''This permission doesnt let users to subscribe/unsubscribe twice'''
    
    def has_permission(self, request, view):
        # The channel token that is passed in url
        channel_token = view.kwargs.get('channel_token')

        # Get subscriber from cache or db
        subscriber = ChannelSubscriber.get_subscriber(
                channel_token=channel_token, 
                user_token=request.user.token
            )
        
        if request.method == 'POST':
            if subscriber and subscriber.get('subscription_status') == 'subscribed':
                self.message = 'You have already subscribed to this channel.'
                return False
            else:
                return True
        
        elif request.method == 'DELETE':
            if not subscriber or subscriber.get('subscription_status') == 'unsubscribed':
                self.message = 'You have not subscribed to this channel yet.'
                return False
            else:
               return True
            
        # If the request.method == "GET" return True
        return True