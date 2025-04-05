from rest_framework.routers import DefaultRouter
from .views import (
    TourOperatorViewSet,
    AttractionTourViewSet,
    ThemeTourViewSet,
    ParticipantTypeTourViewSet,
    FormatTourViewSet,
    DurationTourViewSet,
    SpecialOfferTourViewSet,
    GalleryTourViewSet,
    TourConditionsViewSet,
    AvailableDateTourViewSet,
    OrderViewSet,
    TourViewSet,
)

router = DefaultRouter()

# Основные маршруты
router.register(r"touroperators", TourOperatorViewSet)
router.register(r"tours", TourViewSet)
router.register(r"gallery_tour", GalleryTourViewSet)
router.register(r"order", OrderViewSet)

# Справочники
router.register(r"attractions", AttractionTourViewSet)
router.register(r"themes", ThemeTourViewSet)
router.register(r"participant_types", ParticipantTypeTourViewSet)
router.register(r"formats", FormatTourViewSet)
router.register(r"durations", DurationTourViewSet)
router.register(r"special_offers", SpecialOfferTourViewSet)
router.register(r"tour_conditions", TourConditionsViewSet)
router.register(r"available_dates", AvailableDateTourViewSet)

urlpatterns = router.urls

