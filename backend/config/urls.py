from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

admin.site.site_header = "Tsuna Streaming Admin"


LOCAL_APPS = [
    path("accounts/", include("apps.accounts.urls")),
    path("memberships/", include("apps.memberships.urls")),
    path("channels/", include("apps.channels.urls")),
    path("channel_admins/", include("apps.channel_admins.urls")),
    path("channel_subscribers/", include("apps.channel_subscribers.urls")),
    path("videos/", include("apps.videos.urls")),
    path("musics/", include("apps.musics.urls")),
    path("votes/", include("apps.votes.urls")),
    path("comments/", include("apps.comments.urls")),
    path("viewers/", include("apps.viewers.urls")),
]

THIRD_PARTY_APPS = [
    # Django Debug Toolbar
    path("__debug__/", include("debug_toolbar.urls")),
    # api docs
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("docs/download/", SpectacularAPIView.as_view(), name="schema"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

handler404 = "core.views.error_handler_404"
handler500 = "core.views.error_handler_500"
