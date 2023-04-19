from django.urls import path
from videos.views import VideoListCreateView, VideoDetailView

app_name = "videos"

urlpatterns = [
    path('<str:channel_token>/', VideoListCreateView.as_view(), name='video_list_create'),
    path('<str:channel_token>/<str:video_token>/', VideoDetailView.as_view(), name='video_detail'),
]