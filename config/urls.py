from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

admin.site.site_header = "Tsuna Streaming Admin"


LOCAL_APPS = [
    path("v1/accounts/", include("apps.accounts.urls")),
    path("v1/memberships/", include("apps.memberships.urls")),

    path("v1/channels/", include("apps.channels.urls")),
    path("v1/channel_admins/", include("apps.channel_admins.urls")),
    path("v1/channel_subscribers/", include("apps.channel_subscribers.urls")),

    path("v1/videos/", include("apps.videos.urls")),
    path("v1/musics/", include("apps.musics.urls")),

    path("v1/votes/", include("apps.votes.urls")),
    path("v1/comments/", include("apps.comments.urls")),
    path("v1/viewers/", include("apps.viewers.urls")),    
]

THIRD_PARTY_APPS = [
    # Django Debug Toolbar
    path('__debug__/', include('debug_toolbar.urls')),
    
    # api docs
    path('docs/download/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

urlpatterns = [
    path('admin/', admin.site.urls),

    *THIRD_PARTY_APPS,
    *LOCAL_APPS,

]


handler404 = 'core.views.error_handler_404'
handler500 = 'core.views.error_handler_500'