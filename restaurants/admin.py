from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import RestaurantType, Service, Restaurant, RestaurantImage


class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1
    fields = ("image", "preview")
    readonly_fields = ("preview",)
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"

    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px;" />'
        return "Нет изображения"

    preview.short_description = "Превью"
    preview.allow_tags = True


@admin.register(RestaurantType)
class RestaurantTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description_short")
    search_fields = ("name", "description")
    list_filter = ("name",)

    def description_short(self, obj):
        return obj.description[:50] + "..." if obj.description else ""

    description_short.short_description = "Описание"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "description_short")
    search_fields = ("name", "description")

    def description_short(self, obj):
        return obj.description[:50] + "..." if obj.description else ""

    description_short.short_description = "Описание"


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
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
    list_display = ("restaurant", "preview")
    list_filter = ("restaurant",)
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px;" />'
        return "Нет изображения"

    preview.short_description = "Превью"
    preview.allow_tags = True


# Настройки админ-панели
admin.site.site_header = _("Администрирование ресторанов")
admin.site.site_title = _("Рестораны")
admin.site.index_title = _("Управление контентом")
