from rest_framework.routers import DefaultRouter


from .views import RestaurantViewSet, ReviewRestaurantViewSet

app_name = "restaurants"

router = DefaultRouter()
router.register(r"review", ReviewRestaurantViewSet)
router.register(r"", RestaurantViewSet)

urlpatterns = router.urls
