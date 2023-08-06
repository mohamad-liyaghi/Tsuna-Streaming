from django.urls import path, include
from .views import (
    SubscriberStatusView,
    SubscriberCreateView,
    SubscriberDeleteView,
    SubscriberListView,
)

app_name = 'channel_subscribers'

V1 = [
    path(
        '<str:channel_token>/',
        SubscriberStatusView.as_view(),
        name='subscriber_status'
    ),
    path(
        '<str:channel_token>/create/',
        SubscriberCreateView.as_view(),
        name='create_subscriber'
    ),
    path(
        '<str:channel_token>/delete/',
        SubscriberDeleteView.as_view(),
        name='delete_subscriber'
    ),
    path(
        '<str:channel_token>/list/',
        SubscriberListView.as_view(),
        name='subscriber_list'
    ),
]

urlpatterns = [
    path('v1/', include(V1)),
]
