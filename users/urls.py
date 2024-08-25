from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, OwnerObjectsViewSet, CabinetViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'owner_objects', OwnerObjectsViewSet,
                basename='owner_objects')
router.register(r'cabinet', CabinetViewSet,
                basename='cabinet')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    # JWT-эндпоинты, для управления JWT-токенами:
    path('auth/', include('djoser.urls.jwt'))
]
