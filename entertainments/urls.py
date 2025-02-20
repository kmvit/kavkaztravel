
from rest_framework.routers import DefaultRouter

from .views import EntertainmentReviewViewSet, EntertainmentViewSet

app_name = "entertainments"

router = DefaultRouter()
router.register(r"review", EntertainmentReviewViewSet)
router.register(r"", EntertainmentViewSet)

urlpatterns = router.urls





