from django.urls import path
from .views import (
    VoteStatusView,
    VoteCreateView,
    VoteDeleteView,
    VoteListView
)

app_name = "votes"

urlpatterns = [
    path(
        "<str:content_type_id>/<str:object_token>/",
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
    path(
        "<str:content_type_id>/<str:object_token>/list/",
        VoteListView.as_view(),
        name="list"
    ),
]