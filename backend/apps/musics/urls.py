from django.urls import path, include
from .views import MusicListCreateView, MusicDetailView

app_name = "musics"

V1 = [
    path("<str:channel_token>/", MusicListCreateView.as_view(), name="list_create"),
    path(
        "<str:channel_token>/<str:object_token>/",
        MusicDetailView.as_view(),
        name="detail",
    ),
]

urlpatterns = [
    path("v1/", include(V1)),
]
