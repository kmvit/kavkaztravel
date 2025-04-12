import django_filters
from .models import Tour, TagTour, Region


class TourFilter(django_filters.FilterSet):
    """
    Фильтрация туров с поддержкой:
    - фильтрации по одному региону
    - фильтрации по тегам с логикой И (AND) или ИЛИ (OR)
    - стандартной фильтрации по цене.
    """

    # Фильтрация по тегам с логикой И/ИЛИ
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags",
        queryset=TagTour.objects.all(),
        method="filter_by_tags",  # Указываем метод фильтрации для тэгов
        help_text="Фильтрация по тегам. Используйте tags_mode=AND для логики И, tags_mode=OR для логики ИЛИ.",
    )

    # Фильтрация только по одному региону (используем ModelChoiceFilter вместо ModelMultipleChoiceFilter)
    region = django_filters.ModelChoiceFilter(
        field_name="region",
        queryset=Region.objects.all(),
        help_text="Фильтрация по одному региону.",
    )

    # Фильтрация по цене (стандартные операторы)
    price = django_filters.RangeFilter(
        field_name="price", help_text="Фильтрация по цене в диапазоне (min-max)."
    )

    class Meta:
        model = Tour
        fields = ["tags", "region", "price"]

    def filter_by_tags(self, queryset, name, value):
        """
        Метод для фильтрации с логикой И или ИЛИ по тегам.
        Применяется только к фильтру 'tags'.
        """
        if not value:
            return queryset

        mode = self.request.query_params.get("tags_mode", "OR").upper()

        if mode == "AND":
            # Логика И - все теги должны быть у тура
            qs = queryset
            for tag in value:
                qs = qs.filter(tags=tag)
            return qs

        # Логика ИЛИ (по умолчанию) - туры, у которых есть хотя бы один тег из выбранных
        return queryset.filter(tags__in=value).distinct()
