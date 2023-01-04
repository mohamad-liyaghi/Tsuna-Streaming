from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

admin.site.site_header = "Tsuna Streaming Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    # debug toolbar
    path('__debug__/', include('debug_toolbar.urls')),

    # v1 app urls
    path("v1/accounts/", include("v1.accounts.urls")),

    # api docs
    path('docs/download/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
