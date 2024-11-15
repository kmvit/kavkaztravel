from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path
from Kavkaztome import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Your Project API",
        default_version="v1",
        description="API documentation for Your Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourproject.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/regions/", include("regions.urls")),
    path("api/v1/hotels/", include("hotels.urls")),
    path("api/v1/restaurants/", include("restaurants.urls")),
    path("api/v1/tours/", include("tours.urls")),
    path("api/v1/kashiring/", include("kashiring.urls")),
    path("api/v1/entertainments/", include("entertainments.urls")),
    path("api/v1/users/", include("users.urls")),
    re_path(r"^auth/", include("drf_social_oauth2.urls", namespace="drf")),
    path("api/v1/blog", include("blog.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"
    ),
]
if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
    urlpatterns.extend(
        [
            path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
            path(
                "api/v1/docs/",
                SpectacularSwaggerView.as_view(url_name="schema"),
                name="docs",
            ),
        ]
    )
