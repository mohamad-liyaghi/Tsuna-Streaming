from django.urls import path
from videos.views import VideoListCreateView, VideoDetailView

app_name = "videos"

urlpatterns = [
    path(
        '<str:channel_token>/',
        VideoListCreateView.as_view(),
        name='list_create'
    ),
    path(
        '<str:channel_token>/<str:object_token>/',
        VideoDetailView.as_view(),
        name='detail'
    ),
]