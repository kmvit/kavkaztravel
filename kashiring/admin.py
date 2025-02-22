from django.contrib import admin
from .models import Car, CarFeature, RentalCondition, CarImage


class CarImageInline(admin.TabularInline):
    """Инлайн для добавления изображений автомобиля в карточке машины."""
    model = CarImage
    extra = 1  # Показывать одно пустое поле для загрузки нового изображения


class CarFeatureInline(admin.TabularInline):
    """Инлайн для добавления характеристик автомобиля в карточке машины."""
    model = CarFeature
    extra = 3  # Показывать одно пустое поле для добавления новой характеристики


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Админка для управления автомобилями."""
    list_display = ('brand', 'body_type', 'price_per_day', 'owner')
    list_filter = ('brand', 'body_type', 'price_per_day')
    search_fields = ('brand', 'owner__username')
    ordering = ('brand',)
    inlines = [CarImageInline, CarFeatureInline]  # Инлайны для фото и характеристик


@admin.register(CarFeature)
class CarFeatureAdmin(admin.ModelAdmin):
    """Админка для управления характеристиками автомобилей."""
    list_display = ('car', 'name')
    list_filter = ('name',)
    search_fields = ('car__brand', 'car__owner__username')


@admin.register(RentalCondition)
class RentalConditionAdmin(admin.ModelAdmin):
    """Админка для управления условиями аренды автомобилей."""
    list_display = ('car', 'insurance_deposit', 'min_driver_age', 'min_driving_experience')
    list_filter = ('min_driver_age', 'min_driving_experience')
    search_fields = ('car__brand', 'car__owner__username')


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    """Админка для управления изображениями автомобилей."""
    list_display = ('car', 'image')
    search_fields = ('car__brand', 'car__owner__username')
