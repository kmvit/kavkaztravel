from django_filters import rest_framework as filters
from .models import Car, RentalCondition, Model


class CarFilter(filters.FilterSet):
    """
    Фильтр для автомобилей.
    Позволяет фильтровать по:
    - Модели (model)
    - Типу кузова (body_type)
    - Диапазону цен (price_per_day)
    """

    model = filters.ModelChoiceFilter(queryset=Model.objects.all(), field_name="model", label="Модель")
    body_type = filters.CharFilter(field_name="body_type", lookup_expr="iexact")
    price_per_day_min = filters.NumberFilter(
        field_name="price_per_day", lookup_expr="gte"
    )
    price_per_day_max = filters.NumberFilter(
        field_name="price_per_day", lookup_expr="lte"
    )
    insurance_deposit_min = filters.NumberFilter(
        field_name="insurance_deposit", lookup_expr="gte"
    )
    insurance_deposit_max = filters.NumberFilter(
        field_name="insurance_deposit", lookup_expr="lte"
    )

