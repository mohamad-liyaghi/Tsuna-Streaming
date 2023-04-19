from django.urls import path
from .views import ViewerListView

app_name = 'viewers'

urlpatterns = [
    path("<str:object_token>/", ViewerListView.as_view(), name="viewer_list"),
]
