from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BrandViewSet,
    ModelViewSet,
    ReviewAutoViewSet,
    YearViewSet,
    ColorViewSet,
    BodyTypeViewSet,
    AutoViewSet,
    CompanyAutoViewSet,
    CompanyViewSet,
)

app_name = "kashiring"

router = DefaultRouter()
router.register(r"brands", BrandViewSet, basename="brand")
router.register(r"models", ModelViewSet, basename="model")
router.register(r"years", YearViewSet, basename="year")
router.register(r"colors", ColorViewSet, basename="color")
router.register(r"bodytypes", BodyTypeViewSet, basename="bodytype")
router.register(r"company_autos", CompanyAutoViewSet, basename="company_autos")
router.register(r"company", CompanyViewSet, basename="company")
router.register(r"review", ReviewAutoViewSet, basename="review")
router.register(r"", AutoViewSet, basename="auto")


urlpatterns = router.urls
