from rest_framework.routers import DefaultRouter
from .views import GuideViewSet, TourOperatorViewSet

router = DefaultRouter()
router.register(r'guides', GuideViewSet)
router.register(r'touroperators', TourOperatorViewSet)

urlpatterns = router.urls
