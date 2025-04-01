from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import RestaurantType, Service, Restaurant, RestaurantImage
from django.utils.safestring import mark_safe


class RestaurantImageInline(admin.TabularInline):
    """
    Inline-админка для управления изображениями ресторана.

    Позволяет добавлять и редактировать изображения ресторана непосредственно
    на странице редактирования ресторана в табличном виде.
    """

    model = RestaurantImage
    extra = 1
    fields = ("image", "preview")
    readonly_fields = ("preview",)
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"

    def preview(self, obj):
        """
        Возвращает HTML-код для отображения превью изображения.

        Если изображение загружено, возвращается HTML-тег img с ограниченной высотой.
        В противном случае возвращается строка "Нет изображения".
        """
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px;" />'
        return "Нет изображения"

    preview.short_description = "Превью"
    preview.allow_tags = True


@admin.register(RestaurantType)
class RestaurantTypeAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели RestaurantType.

    Отображает список типов ресторанов с названием и сокращённым описанием.
    Обеспечивает поиск и фильтрацию по полям модели.
    """

    list_display = ("name", "description_short")
    search_fields = ("name", "description")
    list_filter = ("name",)

    def description_short(self, obj):
        return obj.description[:50] + "..." if obj.description else ""

    description_short.short_description = "Описание"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Service.

    Отображает список услуг с названием и сокращённым описанием.
    Обеспечивает возможность поиска по названию и описанию услуги.
    """

    list_display = ("name", "description_short")
    search_fields = ("name", "description")

    def description_short(self, obj):
        """
        Возвращает сокращённое описание услуги.

        Если описание присутствует, возвращает первые 50 символов с добавлением многоточия.
        Если описания нет, возвращает пустую строку.
        """
        return obj.description[:50] + "..." if obj.description else ""

    description_short.short_description = "Описание"


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели Restaurant.

    Отображает основные сведения о ресторане, такие как название, адрес, регион,
    владелец, средний чек и часы работы. Обеспечивает фильтрацию, поиск и редактирование
    связанных объектов, включая услуги и изображения ресторана.
    """

    list_display = (
        "name",
        "address",
        "region",
        "owner",
        "average_check",
        "working_hours",
    )
    list_filter = ("region", "restaurant_type", "owner")
    search_fields = ("name", "address", "description")
    filter_horizontal = ("services",)
    inlines = (RestaurantImageInline,)
    fieldsets = (
        (None, {"fields": ("name", "address", "owner")}),
        (
            "Детали",
            {"fields": ("region", "restaurant_type", "average_check", "working_hours")},
        ),
        ("Описание и услуги", {"fields": ("description", "services")}),
    )


@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    """
    Административный интерфейс для модели RestaurantImage.

    Позволяет просматривать список изображений с привязкой к ресторанам и
    отображать превью изображений в виде HTML-кода.
    """

    list_display = ("restaurant", "preview")
    list_filter = ("restaurant",)
    readonly_fields = ("preview",)

    def preview(self, obj):
        """
        Возвращает HTML-код для отображения превью изображения ресторана.

        Если изображение доступно, возвращается HTML-тег img с ограничением по высоте.
        В противном случае возвращается строка "Нет изображения".

        :param obj: Экземпляр модели RestaurantImage.
        :return: HTML-строка или сообщение об отсутствии изображения.
        """
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 100px;" />'
            )
        return "Нет изображения"

    preview.short_description = "Превью"
    preview.allow_tags = True


# Настройки админ-панели
admin.site.site_header = _("Администрирование ресторанов")
admin.site.site_title = _("Рестораны")
admin.site.index_title = _("Управление контентом")
