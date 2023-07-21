from django.urls import path
from .views import (
    SubscriberStatusView,
    SubscriberListView,
    SubscriberView
)

app_name = 'channel_subscribers'

urlpatterns = [
    path(
        '<str:channel_token>/',
        SubscriberStatusView.as_view(),
        name='subscriber_status'
    ),
    path('<str:channel_token>/', SubscriberView.as_view(), name='subscriber'),
    path('<str:channel_token>/list', SubscriberListView.as_view(), name='subscriber_list')
]
