from django.urls import path
from .views import VoteView, VoteListView

app_name = "v1_votes"

urlpatterns = [
    path("<str:object_token>/", VoteView.as_view(), name="vote"),
    path("<str:object_token>/list/", VoteListView.as_view(), name="vote_list"),
]