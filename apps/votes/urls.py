from django.urls import path
from .views import (
    VoteStatusView,
    VoteCreateView,
    VoteDeleteView,
    VoteView,
    VoteListView
)

app_name = "votes"

urlpatterns = [
    path(
        "<str:content_type_id>/<str:object_token>/status/",
        VoteStatusView.as_view(),
        name='status'
    ),
    path(
        "<str:content_type_id>/<str:object_token>/create/",
        VoteCreateView.as_view(),
        name='create'
    ),
    path(
        "<str:content_type_id>/<str:object_token>/delete/",
        VoteDeleteView.as_view(),
        name='delete'
    ),
    path("<str:object_token>/", VoteView.as_view(), name="vote"),
    path("<str:object_token>/list/", VoteListView.as_view(), name="vote_list"),
]