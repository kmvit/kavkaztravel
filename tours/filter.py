import django_filters
from .models import Tour


class TourFilter(django_filters.FilterSet):
    """
    Фильтр для получения информации по турам из модели Tour.

    Может фильтровать по тэгам, турам, тегам и турам.
    """

    geo = django_filters.CharFilter(
        field_name="geo__geo_title", lookup_expr="icontains"
    )
    tag = django_filters.CharFilter(field_name="tag__name", lookup_expr="icontains")

    class Meta:
        model = Tour
        fields = ["geo", "tag"]
