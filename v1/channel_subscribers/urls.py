from django.urls import path
from . import views

app_name = 'v1_channel_subscribers'

urlpatterns = [
    path('<str:channel_token>/', views.SubscriberView.as_view(), name='subscriber_view')
]
