from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from Kavkaztome import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Подключаем API разных приложений
    path("api/v1/regions/", include("regions.urls")),
    path("api/v1/hotels/", include("hotels.urls")),
    path("api/v1/restaurants/", include("restaurants.urls")),
    path("api/v1/tours/", include("tours.urls")),
    path("api/v1/kashiring/", include("kashiring.urls")),
    path("api/v1/entertainments/", include("entertainments.urls")),
    path("api/v1/users/", include("users.urls")),
    path("api/v1/reviews/", include("reviews.urls")),
    path("api/v1/blog/", include("blog.urls")),
    
    # OAuth авторизация
    re_path(r"^auth/", include("drf_social_oauth2.urls", namespace="drf")),

    # DRF Spectacular: схема API и документация
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

# Раздача медиафайлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
