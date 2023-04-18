from django.urls import path
from .views import MusicListCreateView

app_name = 'v1_musics'

urlpatterns = [
    path('<str:channel_token>/', MusicListCreateView.as_view(), name='music_list_create'),
]
