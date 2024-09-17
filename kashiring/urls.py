from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BrandViewSet, ModelViewSet, YearViewSet, ColorViewSet, BodyTypeViewSet,
    AutoViewSet, FotoViewSet, CompanyViewSet
)

# Создаем роутер и регистрируем в нем наши viewsets
router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'models', ModelViewSet, basename='model')
router.register(r'years', YearViewSet, basename='year')
router.register(r'colors', ColorViewSet, basename='color')
router.register(r'bodytypes', BodyTypeViewSet, basename='bodytype')
router.register(r'autos', AutoViewSet, basename='auto')
router.register(r'photos', FotoViewSet, basename='photo')
router.register(r'companies', CompanyViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls)),
]
