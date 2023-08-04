from django.urls import path
from .views import MusicListCreateView, MusicDetailView

app_name = 'musics'

urlpatterns = [
    path(
        '<str:channel_token>/',
        MusicListCreateView.as_view(),
        name='list_create'
    ),
    path(
        '<str:channel_token>/<str:object_token>/',
        MusicDetailView.as_view(),
        name='detail'
    ),
]
