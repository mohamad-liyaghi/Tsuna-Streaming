from django.urls import path
from .views import MusicListCreateView, MusicDetailView

app_name = 'musics'

urlpatterns = [
    path('<str:channel_token>/', MusicListCreateView.as_view(), name='music_list_create'),
    path('<str:channel_token>/<str:music_token>/', MusicDetailView.as_view(), name='music_detail'),
]
