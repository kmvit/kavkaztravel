from django_filters import rest_framework as filters
from .models import Restaurant, Region, Service, RestaurantType


class RestaurantFilter(filters.FilterSet):
    """
    Фильтр для модели Restaurant.

    Позволяет фильтровать рестораны по следующим критериям:
      - Название региона (без учета регистра).
      - Минимальный и максимальный диапазон среднего чека.
      - Тип заведения (без учета регистра).
      - Услуги ресторана по полному совпадению названия.

    Каждый фильтр использует соответствующий lookup выражение для точного и гибкого поиска.
    """

    # Фильтр по названию региона
    region = filters.CharFilter(
        field_name="region__name", lookup_expr="icontains", label="Название региона"
    )

    # Фильтр по диапазону среднего чека
    average_check_min = filters.NumberFilter(
        field_name="average_check", lookup_expr="gte", label="Минимальный средний чек"
    )
    average_check_max = filters.NumberFilter(
        field_name="average_check", lookup_expr="lte", label="Максимальный средний чек"
    )

    # Фильтр по типу заведения
    restaurant_type = filters.CharFilter(
        field_name="restaurant_type__name",
        lookup_expr="icontains",
        label="Тип заведения",
    )

    # Фильтр по услугам (полное совпадение названия)
    services = filters.ModelMultipleChoiceFilter(
        field_name="services__name",
        to_field_name="name",
        queryset=Service.objects.all(),
        label="Услуги",
    )

    class Meta:
        model = Restaurant
        fields = []
