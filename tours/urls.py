from rest_framework.routers import DefaultRouter
from .views import (
    TourOperatorViewSet,
    TagTourViewSet,
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
router.register(r"tag", TagTourViewSet)
router.register(r"available_dates", AvailableDateTourViewSet)

urlpatterns = router.urls

