"""
URL configuration for Backend project.

"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("api/", include("Post.urls")),
    path("api/", include("Auth.urls")),
    path("api/", include("Users.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
