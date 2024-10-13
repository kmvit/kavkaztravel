import django_filters
from .models import Tour

class TourFilter(django_filters.FilterSet):
    geo = django_filters.CharFilter(field_name='geo__geo_title', lookup_expr='icontains')  # Убедитесь, что 'name' существует в Geo
    tag = django_filters.CharFilter(field_name='tag__name', lookup_expr='icontains')  # Убедитесь, что 'name' существует в Tag
    class Meta:
        model = Tour
        fields = ['geo', 'tag']