from django.urls import path
from .views import ViewerListView

app_name = 'v1_viewers'

urlpatterns = [
    path("viewer/<str:content_type_id>/<str:token>/", ViewerListView.as_view(), name="viewer_list"),
]
