from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Car, CarImage, RentalCondition, CarFeature, RentalDiscount
from .serializers import (
    CarSerializer,
    CarImageSerializer,
    RentalConditionSerializer,
    CarCreateUpdateSerializer,
    RentalSerializer,
    RentalDiscountSerializer,
)
from .filters import CarFilter, RentalConditionFilter
from .swagger_docs import (
    CarSwagger,
    CarImageSwagger,
    RentalConditionSwagger,
    RentalDiscountSwagger,
    RentalSwagger,
)
from .permissions import IsOwnerOrReadOnly


class CarViewSet(viewsets.ModelViewSet):
    """API для управления автомобилями."""

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Оптимизированный запрос с prefetch_related:
        - Подгружаем характеристики автомобиля (features)
        - Подгружаем изображения автомобиля (images)
        - Подгружаем тарифный план (discount_policy)
        """
        return Car.objects.prefetch_related(
            Prefetch(
                "features", queryset=CarFeature.objects.all(), to_attr="features_list"
            ),
            Prefetch("images", queryset=CarImage.objects.all(), to_attr="images_list"),
            Prefetch(
                "discount_policy",
                queryset=RentalDiscount.objects.all(),
                to_attr="discount_policy_obj",
            ),
        )

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CarCreateUpdateSerializer
        return CarSerializer

    @CarSwagger.car_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @CarSwagger.car_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @CarSwagger.car_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @CarSwagger.car_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @CarSwagger.car_update
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @CarSwagger.car_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CarImageViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """API для управления изображениями автомобилей."""

    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    @CarImageSwagger.image_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @CarImageSwagger.image_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @CarImageSwagger.image_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @CarImageSwagger.image_delete
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class RentalConditionViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """API для управления условиями аренды автомобилей."""

    queryset = RentalCondition.objects.all()
    serializer_class = RentalConditionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RentalConditionFilter

    @RentalConditionSwagger.rental_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @RentalConditionSwagger.rental_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @RentalConditionSwagger.rental_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @RentalConditionSwagger.rental_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @RentalConditionSwagger.rental_update
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class RentalDiscountViewSet(viewsets.ModelViewSet):
    """
    API для управления тарифными планами (скидками на аренду).
    """

    queryset = RentalDiscount.objects.all()
    serializer_class = RentalDiscountSerializer

    @RentalDiscountSwagger.discount_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @RentalDiscountSwagger.discount_create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @RentalDiscountSwagger.discount_detail
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @RentalDiscountSwagger.discount_update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @RentalDiscountSwagger.discount_update
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class RentalCreateView(APIView):
    """Эндпоинт для создания аренды и возврата рассчитанной стоимости"""

    @RentalSwagger.rental_create
    def post(self, request, *args, **kwargs):
        serializer = RentalSerializer(data=request.data)
        if serializer.is_valid():
            rental = serializer.save()

            # Безопасное приведение к float (или str, если вдруг возникнет проблема сериализации)
            total_price = rental.calculate_total_price_with_discount()
            total_price = (
                float(total_price)
                if isinstance(total_price, (int, float))
                else str(total_price)
            )

            return Response(
                {"rental_id": rental.id, "total_price": total_price}, status=201
            )
        return Response(serializer.errors, status=400)
