from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

admin.site.site_header = "Tsuna Streaming Admin"


LOCAL_APPS = [
    path("v1/accounts/", include("v1.accounts.urls")),
    path("v1/memberships/", include("v1.memberships.urls")),

    path("v1/channels/", include("v1.channels.urls")),
    path("v1/channel_admins/", include("v1.channel_admins.urls")),
    path("v1/channel_subscribers/", include("v1.channel_subscribers.urls")),

    path("v1/videos/", include("v1.videos.urls")),
    path("v1/musics/", include("v1.musics.urls")),

    path("v1/votes/", include("v1.votes.urls")),
    path("v1/comments/", include("v1.comments.urls")),
    path("v1/viewers/", include("v1.viewers.urls")),    
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