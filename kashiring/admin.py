from django.contrib import admin
from .models import Car, CarFeature, RentalCondition, CarImage, Rental, RentalDiscount


class CarImageInline(admin.TabularInline):
    """Инлайн для добавления изображений автомобиля в карточке машины."""

    model = CarImage
    extra = 1  # Показывать одно пустое поле для загрузки нового изображения


class CarFeatureInline(admin.TabularInline):
    """Инлайн для добавления характеристик автомобиля в карточке машины."""

    model = CarFeature
    extra = 3  # Показывать одно пустое поле для добавления новой характеристики


@admin.register(RentalDiscount)
class RentalDiscountAdmin(admin.ModelAdmin):
    """Админка для управления скидками на аренду."""

    list_display = ("name", "discount_week", "discount_month")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Админка для автомобилей."""

    list_display = (
        "id",
        "brand",
        "body_type",
        "price_per_day",
        "owner",
        "discount_policy",
    )
    list_filter = ("brand", "body_type", "discount_policy")
    search_fields = ("brand", "owner__username")
    ordering = ("brand",)
    inlines = [CarImageInline, CarFeatureInline]  # Инлайны для фото и характеристик


@admin.register(CarFeature)
class CarFeatureAdmin(admin.ModelAdmin):
    """Админка для управления характеристиками автомобилей."""

    list_display = ("car", "name")
    list_filter = ("name",)
    search_fields = ("car__brand", "car__owner__username")


@admin.register(RentalCondition)
class RentalConditionAdmin(admin.ModelAdmin):
    """Админка для управления условиями аренды автомобилей."""

    list_display = (
        "car",
        "insurance_deposit",
        "min_driver_age",
        "min_driving_experience",
        "required_documents",
    )
    list_filter = ("min_driver_age", "min_driving_experience")
    search_fields = ("car__brand", "car__owner__username")


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    """Админка для управления изображениями автомобилей."""

    list_display = ("car", "image")
    search_fields = ("car__brand", "car__owner__username")


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "car",
        "pickup_datetime",
        "return_datetime",
        "total_price_display",
        "return_location",
    )
    search_fields = ("user__username", "car__id")
    list_filter = ("pickup_datetime", "return_datetime")
    readonly_fields = ("total_price_display",)

    def total_price_display(self, obj):
        """
        Отображение итоговой стоимости в админке с учетом скидок.
        """
        if not obj.car or not obj.pickup_datetime or not obj.return_datetime:
            return "Не указано"

        rental_days = (obj.return_datetime - obj.pickup_datetime).days
        if rental_days < 1:
            return "Ошибка дат"

        total_price = obj.car.calculate_rental_price(rental_days)
        return f"{total_price:.2f} ₽"

    total_price_display.short_description = "Общая стоимость"
