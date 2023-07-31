from django.urls import path
from .views import ViewerListView

app_name = 'viewers'

urlpatterns = [
    path(
        "<str:content_type_id>/<str:object_token>/list/",
        ViewerListView.as_view(),
        name="list",
    )
]
