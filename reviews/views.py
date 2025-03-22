from django.db.models import Avg, Count
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import CarReview, CarReviewImage, CarRating, Car
from .serializers import (
    CarReviewDetailSerializer,
    CarReviewCreateUpdateSerializer,
    CarReviewImageSerializer,
    CarReviewListSerializer,
)
from .pagination import ReviewPagination
from .permissions import IsOwnerOrReadOnly
from .swagger_schemas import (
    car_review_create,
    car_review_car,
    car_review_detail,
    car_review_update,
    car_review_replace,
    car_review_delete,
    car_review_image_upload,
    car_review_image_list,
    car_review_image_detail,
    car_review_image_update,
    car_review_image_delete,
)


class CarReviewViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """CRUD для отзывов автомобиля."""

    queryset = CarReview.objects.select_related("user", "car").prefetch_related(
        "ratings", "car_images"
    )
    pagination_class = ReviewPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """Фильтрация: админ видит всё, пользователи – только одобренные отзывы автомобиля."""
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(is_approved=True)

    def get_serializer_class(self):
        """Используем разные сериализаторы для GET и POST/PUT автомобиля."""
        if self.action == "retrieve":
            return CarReviewDetailSerializer
        return CarReviewCreateUpdateSerializer

    @car_review_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @car_review_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @car_review_car
    @action(detail=False, methods=["get"], url_path="reviews_car")
    def car_reviews_for_car(self, request):
        """Получение всех одобренных отзывов для конкретного автомобиля с добавлением средних оценок."""

        car_id = request.query_params.get("car_id")

        if not car_id:
            return Response(
                {"error": "car_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        car = Car.objects.filter(id=car_id).first()
        if not car:
            return Response(
                {"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND
            )

        average_rating = CarReview.get_average_rating(car)
        review_count = CarReview.get_review_count(car)

        reviews = CarReview.objects.filter(car=car, is_approved=True)

        criteria_averages = (
            CarRating.objects.filter(car_review__car=car)
            .values("criteria")
            .annotate(avg_score=Avg("score"))
        )

        averages = {
            "cleanliness_avg": next(
                (
                    item["avg_score"]
                    for item in criteria_averages
                    if item["criteria"] == "cleanliness"
                ),
                0,
            ),
            "service_avg": next(
                (
                    item["avg_score"]
                    for item in criteria_averages
                    if item["criteria"] == "service"
                ),
                0,
            ),
            "location_avg": next(
                (
                    item["avg_score"]
                    for item in criteria_averages
                    if item["criteria"] == "location"
                ),
                0,
            ),
            "photo_match_avg": next(
                (
                    item["avg_score"]
                    for item in criteria_averages
                    if item["criteria"] == "photo_match"
                ),
                0,
            ),
            "price_quality_avg": next(
                (
                    item["avg_score"]
                    for item in criteria_averages
                    if item["criteria"] == "price_quality"
                ),
                0,
            ),
        }
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = CarReviewListSerializer(page, many=True)
            response_data = serializer.data

            return Response(
                {
                    "results": response_data,
                    "review_count": review_count,
                    "average_rating": average_rating,
                    "averages": averages,
                }
            )

        return Response({"error": "No reviews found"}, status=status.HTTP_404_NOT_FOUND)

    @car_review_replace
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @car_review_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CarReviewImageViewSet(viewsets.ModelViewSet):
    """CRUD для загрузки изображений к отзывам автомобиля."""

    queryset = CarReviewImage.objects.all()
    serializer_class = CarReviewImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    @car_review_image_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @car_review_image_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @car_review_image_upload
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @car_review_image_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @car_review_image_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
