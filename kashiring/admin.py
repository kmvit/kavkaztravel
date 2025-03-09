from django.contrib import admin
from .models import (
    Car,
    CarFeature,
    CarOption,
    CarEquipment,
    RentalCondition,
    CarImage,
    Rental,
    RentalDiscount,
    Model, 
    Brand
)


class CarImageInline(admin.TabularInline):
    """Инлайн для добавления изображений автомобиля в карточке машины."""
    model = CarImage
    extra = 1  # Показывать одно пустое поле для загрузки нового изображения


class CarFeatureInline(admin.TabularInline):
    """Инлайн для добавления характеристик автомобиля в карточке машины."""
    model = CarFeature
    extra = 3  # Показывать три пустых поля для добавления новых характеристик


class CarOptionInline(admin.TabularInline):
    """Инлайн для дополнительных опций автомобиля."""
    model = CarOption
    extra = 2  # Показывать два пустых поля


class CarEquipmentInline(admin.TabularInline):
    """Инлайн для комплектаций автомобиля."""
    model = CarEquipment
    extra = 2


@admin.register(RentalDiscount)
class RentalDiscountAdmin(admin.ModelAdmin):
    """Админка для управления скидками на аренду."""
    list_display = ("name", "discount_week", "discount_month")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Админка для автомобилей."""
    list_display = ("id", "brand", "body_type", "price_per_day", "owner", "discount_policy")
    list_filter = ("brand", "body_type", "discount_policy")
    search_fields = ("brand__name", "owner__username")
    ordering = ("brand",)
    inlines = [CarImageInline, CarFeatureInline, CarOptionInline, CarEquipmentInline]


@admin.register(CarFeature)
class CarFeatureAdmin(admin.ModelAdmin):
    """Админка для управления характеристиками автомобилей."""
    list_display = ("car", "name")
    list_filter = ("name",)
    search_fields = ("car__brand__name", "car__owner__username")


@admin.register(CarOption)
class CarOptionAdmin(admin.ModelAdmin):
    """Админка для управления опциями автомобилей."""
    list_display = ("car", "name", "price")
    list_filter = ("name",)
    search_fields = ("car__brand__name", "car__owner__username")


@admin.register(CarEquipment)
class CarEquipmentAdmin(admin.ModelAdmin):
    """Админка для управления комплектацией автомобилей."""
    list_display = ("car", "name")
    search_fields = ("car__brand__name", "car__owner__username")


@admin.register(RentalCondition)
class RentalConditionAdmin(admin.ModelAdmin):
    """Админка для управления условиями аренды автомобилей."""
    list_display = ("car", "insurance_deposit", "min_driver_age", "min_driving_experience", "required_documents")
    list_filter = ("min_driver_age", "min_driving_experience")
    search_fields = ("car__brand__name", "car__owner__username")


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    """Админка для управления изображениями автомобилей."""
    list_display = ("car", "image")
    search_fields = ("car__brand__name", "car__owner__username")


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    """Админка для управления арендой автомобилей."""
    list_display = ("user", "car", "pickup_datetime", "return_datetime", "total_price_display", "return_location")
    search_fields = ("user__username", "car__brand__name")
    list_filter = ("pickup_datetime", "return_datetime")
    readonly_fields = ("total_price_display",)

    def total_price_display(self, obj):
        """
        Отображение итоговой стоимости аренды в админке с учетом скидок.
        """
        if not obj.car or not obj.pickup_datetime or not obj.return_datetime:
            return "Не указано"
        
        total_price = obj.calculate_total_price()
        return f"{total_price:.2f} ₽" if total_price is not None else "Ошибка расчёта"

    total_price_display.short_description = "Общая стоимость"

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)