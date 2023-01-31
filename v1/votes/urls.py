from django.urls import path
from .views import RateView

app_name = "v1_votes"

urlpatterns = [
    path("vote/<str:content_type_id>/<str:token>/", RateView.as_view(), name="vote"),
]