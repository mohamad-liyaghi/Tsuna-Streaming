from django.urls import path
from .views import VoteView, VoteListView

app_name = "v1_votes"

urlpatterns = [
    path("vote/<str:content_type_id>/<str:token>/", VoteView.as_view(), name="vote"),
    path("vote-list/<str:content_type_id>/<str:token>/", VoteListView.as_view(), name="vote_list"),
]