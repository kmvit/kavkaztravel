import django_filters
from django_filters import rest_framework as filters
from .models import Hotel, MealPlan, AccommodationType, Amenity, RoomPrice


class HotelFilter(filters.FilterSet):
    meal_plan = filters.ModelMultipleChoiceFilter(
        queryset=MealPlan.objects.all(),
        field_name='meal_plan__name',
        to_field_name='name',
        conjoined=True,
    )
    accommodation_type = filters.ModelMultipleChoiceFilter(
        queryset=AccommodationType.objects.all(),
        field_name='accommodation_type__name',
        to_field_name='name',
        conjoined=True,
    )
    amenities = filters.ModelMultipleChoiceFilter(
        queryset=Amenity.objects.all(),
        field_name='amenities__name',
        to_field_name='name',
        conjoined=True,
    )
    min_price = filters.NumberFilter(
        field_name='rooms__prices__price', lookup_expr='gte'
    )
    max_price = filters.NumberFilter(
        field_name='rooms__prices__price', lookup_expr='lte'
    )
    date = filters.DateFilter(
        field_name='rooms__prices__date', lookup_expr='exact'
    )

    class Meta:
        model = Hotel
        fields = ['meal_plan', 'accommodation_type', 'amenities', 'min_price',
                  'max_price', 'date']
