from rest_framework.routers import DefaultRouter
from .views import (
    HotelViewSet,
    ReviewHotelViewSet,
    RoomViewSet,
    RoomImageViewSet,
    MealPlanViewSet,
    AccommodationTypeViewSet,
    AmenityViewSet,
)

app_name = "hotels"

router = DefaultRouter()

router.register(r"rooms", RoomViewSet)
router.register(r"room_images", RoomImageViewSet)
router.register(r"meal_plans", MealPlanViewSet)
router.register(r"accommodation_types", AccommodationTypeViewSet)
router.register(r"amenities", AmenityViewSet)
router.register(r"review", ReviewHotelViewSet, basename="review")
router.register(r"", HotelViewSet)

urlpatterns = router.urls
