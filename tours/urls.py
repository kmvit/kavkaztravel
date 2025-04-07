from rest_framework.routers import DefaultRouter
from .views import (
    TourOperatorViewSet,
    TourViewSet,
    AvailableDateTourViewSet,

    GalleryTourViewSet,
    OrderViewSet,
    TourViewSet,
)

router = DefaultRouter()

# Основные маршруты
router.register(r"touroperators", TourOperatorViewSet)
router.register(r"tours", TourViewSet)
router.register(r"gallery_tour", GalleryTourViewSet)
router.register(r"order", OrderViewSet)
router.register(r"available_dates", AvailableDateTourViewSet)

urlpatterns = router.urls

