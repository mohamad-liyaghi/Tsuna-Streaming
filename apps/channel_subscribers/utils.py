from enum import Enum


class SubscriberStatus(Enum):
    """
    Subscribers in cache must have one of these 2 statuses:
    - subscribed: the subscriber is subscribed to the channel
    - unsubscribed: the subscriber is unsubscribed from the channel (but still in db)
    """
    SUBSCRIBED = 'subscribed'
    UNSUBSCRIBED = 'unsubscribed'

