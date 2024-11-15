from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EntertainmentViewSet, ReviewEntertainmentViewSet

router = DefaultRouter()
router.register(r"entertainments", EntertainmentViewSet)
router.register(r"review", ReviewEntertainmentViewSet)
app_name = "entertainments"


urlpatterns = router.urls
