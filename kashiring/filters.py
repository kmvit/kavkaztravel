from django_filters import rest_framework as filters
from .models import Car, RentalCondition


class CarFilter(filters.FilterSet):
    """
    Фильтр для автомобилей.
    Позволяет фильтровать по:
    - Типу кузова
    - Диапазону цен
    - Наличию определенных характеристик
    """
    body_type = filters.CharFilter(field_name="body_type", lookup_expr="iexact")
    price_min = filters.NumberFilter(field_name="price_per_day", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price_per_day", lookup_expr="lte")
    features = filters.CharFilter(field_name="features__name", lookup_expr="icontains")

    class Meta:
        model = Car
        fields = []


class RentalConditionFilter(filters.FilterSet):
    """
    Фильтр для условий аренды.
    Позволяет фильтровать по страховому депозиту в заданном диапазоне.
    """
    insurance_deposit_min = filters.NumberFilter(field_name="insurance_deposit", lookup_expr="gte")
    insurance_deposit_max = filters.NumberFilter(field_name="insurance_deposit", lookup_expr="lte")

    class Meta:
        model = RentalCondition
        fields = []
