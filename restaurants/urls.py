from rest_framework.routers import DefaultRouter

from .serializers import ReviewRestaurantGetSerializer
from .views import RestaurantViewSet, ReviewRestaurantViewSet

app_name = "restaurants"

router = DefaultRouter()
router.register(r"restaurants", RestaurantViewSet)
router.register(r"review", ReviewRestaurantViewSet)

urlpatterns = router.urls
