from django.urls import path
from .views import VoteView, VoteListView

app_name = "v1_votes"

urlpatterns = [
    path("vote/<str:object_token>/", VoteView.as_view(), name="vote"),
    path("vote/<str:content_type_id>/<str:object_token>/list/", VoteListView.as_view(), name="vote_list"),
]