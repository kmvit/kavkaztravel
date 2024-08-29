from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from Kavkaztome import settings

schema_view = get_schema_view(
   openapi.Info(
      title="Your Project API",
      default_version='v1',
      description="API documentation for Your Project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourproject.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('regions.urls')),
    path('api/', include('hotels.urls')),
    path('api/', include('restaurants.urls')),
    path('api/', include('tours.urls')),
    path('api/', include('attractions.urls')),
    path('api/', include('entertainments.urls')),
    path('api/', include('users.urls')),
    path('api/', include('reviews.urls')),
    path('api/', include('blog.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='docs'),
]
if settings.DEBUG:
    urlpatterns.extend(
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
    urlpatterns.extend(
        [

            path('api/v1/schema/', SpectacularAPIView.as_view(),
                 name='schema'),
            path('api/v1/docs/',
                 SpectacularSwaggerView.as_view(url_name='schema'),
                 name='docs'),
        ]
    )