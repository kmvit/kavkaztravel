from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Q

from .models import Car, CarImage, RentalCondition, CarFeature, RentalDiscount, CarOption, CarEquipment
from .serializers import (
    Rental,
    CarSerializer,
    CarListSerializer,
    CarImageSerializer,
    RentalConditionSerializer,
    CarCreateUpdateSerializer,
    RentalSerializer,
    RentalDiscountSerializer,
)
from .swagger_docs import (
    CarSwagger,
    CarImageSwagger,
    RentalConditionSwagger,
    RentalDiscountSwagger,
    RentalSwagger,
    CarOptionSerializer, 
    CarEquipmentSerializer,
    CarOptionSwagger, 
    CarEquipmentSwagger
)
from .permissions import IsOwnerOrReadOnly
from .filters import CarFilter


class CarViewSet(viewsets.ModelViewSet):
    """API для управления автомобилями."""

    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        API для управления автомобилями.
        
        Метод get_queryset оптимизирован для различных действий API:
        
        - В режиме 'retrieve' (получение одного автомобиля) загружаются все связанные данные:
        - Особенности автомобиля (`CarFeature`), доступные через `features_list`.
        - Изображения автомобиля (`CarImage`), доступные через `images_list`.
        - Политики скидок (`RentalDiscount`), доступные через `discount_policy_obj`.
        - Опции автомобиля (`CarOption`), доступные через `options_list`.
        - Оборудование (`CarEquipment`), доступное через `equipments_list`.
        
        - В режиме 'list' (получение списка автомобилей) загружаются минимально необходимые данные:
        - Связанный бренд автомобиля (`brand`) загружается через `select_related`.
        - Первое изображение (`CarImage`) сортируется по `id` и доступно через `first_image`.
        - Загружаются только ключевые поля: `id`, `brand__name`, `year_of_production`, `engine_power`, `drive_type`, `engine_type`, `price_per_day`.
        
        - Исключаются автомобили, находящиеся в аренде на текущую дату. Это достигается с помощью запроса в `Rental`, который проверяет, 
        если текущая дата (`today`) попадает в диапазон аренды (`pickup_datetime` ≤ today ≤ `return_datetime`).
        """
        today = now()
        rented_cars = Rental.objects.filter(
            Q(return_datetime__gte=today)
        ).values_list("car_id", flat=True)
        
        if self.action == 'retrieve':
            return Car.objects.filter(~Q(id__in=rented_cars)).prefetch_related(
                Prefetch("features", queryset=CarFeature.objects.all(), to_attr="features_list"),
                Prefetch("images", queryset=CarImage.objects.all(), to_attr="images_list"),
                Prefetch("discount_policy", queryset=RentalDiscount.objects.all(), to_attr="discount_policy_obj"),
                Prefetch("options", queryset=CarOption.objects.all(), to_attr="options_list"),
                Prefetch("equipments", queryset=CarEquipment.objects.all(), to_attr="equipments_list"),
            )
        
        return Car.objects.filter(~Q(id__in=rented_cars)).select_related("brand").prefetch_related(
            Prefetch("images", queryset=CarImage.objects.only("image").order_by("id"), to_attr="first_image"),
        ).only("id", "brand__name", "year_of_production", "engine_power", "drive_type", "engine_type", "price_per_day")

    def get_serializer_class(self):
        if self.action == "list":
            return CarListSerializer
        elif self.action in ["create", "update", "partial_update"]:
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


class CarOptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления дополнительными опциями автомобилей.
    """
    queryset = CarOption.objects.all()
    serializer_class = CarOptionSerializer


class CarEquipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления комплектациями автомобилей.
    """
    queryset = CarEquipment.objects.all()
    serializer_class = CarEquipmentSerializer


class CarOptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления дополнительными опциями автомобилей.
    """

    queryset = CarOption.objects.all()
    serializer_class = CarOptionSerializer

    @CarOptionSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @CarOptionSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @CarOptionSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @CarOptionSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @CarOptionSwagger.partial_update
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @CarOptionSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CarEquipmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления комплектациями автомобилей.
    """

    queryset = CarEquipment.objects.all()
    serializer_class = CarEquipmentSerializer

    @CarEquipmentSwagger.list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @CarEquipmentSwagger.create
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @CarEquipmentSwagger.retrieve
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @CarEquipmentSwagger.update
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @CarEquipmentSwagger.partial_update
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @CarEquipmentSwagger.destroy
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
