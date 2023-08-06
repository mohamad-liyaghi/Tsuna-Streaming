from django.urls import path, include
from .views import ViewerListView

app_name = 'viewers'

V1 = [
    path(
        "<str:content_type_id>/<str:object_token>/list/",
        ViewerListView.as_view(),
        name="list",
    )
]

urlpatterns = [
    path("v1/", include(V1)),
]
