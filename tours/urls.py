from rest_framework.routers import DefaultRouter


from .views import (
    DateTourViewSet,
    GalleryTourViewSet,
    GeoViewSet,
    GuideViewSet,
    OrderViewSet,
    TagViewSet,
    TourOperatorViewSet,
    TourViewSet,
    ReviewTourViewSet,
)

router = DefaultRouter()
router.register(r"guides", GuideViewSet)
router.register(r"touroperators", TourOperatorViewSet)
router.register(r"gallery_tour", GalleryTourViewSet)
router.register(r"date_tour", DateTourViewSet)
router.register(r"tag", TagViewSet)
router.register(r"geo", GeoViewSet)
router.register(r"order", OrderViewSet)
router.register(r"review", ReviewTourViewSet)
router.register(r"", TourViewSet)

urlpatterns = router.urls
