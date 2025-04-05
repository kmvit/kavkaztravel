from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Tour, AttractionTour, ThemeTour, ParticipantTypeTour,
    FormatTour, DurationTour, SpecialOfferTour,
    GalleryTour, TourConditions, AvailableDateTour, Order
)

# Inline-классы для связанных моделей
class TourConditionsInline(admin.TabularInline):
    model = TourConditions
    extra = 1
    fields = ('group_size', 'children', 'meeting_point', 'booking_terms', 'organizational_details')
    verbose_name = "Условие тура"
    verbose_name_plural = "Условия проведения тура"

class GalleryTourInline(admin.TabularInline):
    model = GalleryTour
    extra = 1
    fields = ('image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Превью"

class AvailableDateTourInline(admin.TabularInline):
    model = AvailableDateTour
    extra = 1
    fields = ('start_date', 'end_date', 'is_active')
    verbose_name = "Доступная дата"
    verbose_name_plural = "Доступные даты проведения"

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    fields = ('date', 'size', 'username', 'email', 'phone')
    readonly_fields = ('date', 'size', 'username', 'email', 'phone')
    verbose_name = "Заказ"
    verbose_name_plural = "Заказы тура"

# Основной класс админки для Tour
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'region', 'price', 'duration', 'created_at')
    list_filter = ('region', 'theme', 'duration', 'special_offer')
    search_fields = ('title', 'description')
    filter_horizontal = ('attractions', 'participant_types', 'formats')
    readonly_fields = ('created_at',)
    
    inlines = [
        TourConditionsInline,
        GalleryTourInline,
        AvailableDateTourInline,
        OrderInline,
    ]
    
    fieldsets = (
        (None, {
            'fields': ('guide', 'title', 'description', 'region')
        }),
        ('Основные параметры', {
            'fields': ('price', 'theme', 'duration', 'special_offer')
        }),
        ('Дополнительные параметры', {
            'fields': ('attractions', 'participant_types', 'formats'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

# Админки для остальных моделей
@admin.register(AttractionTour)
class AttractionTourAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region',)
    search_fields = ('name', 'description')

@admin.register(ThemeTour)
class ThemeTourAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(ParticipantTypeTour)
class ParticipantTypeTourAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(FormatTour)
class FormatTourAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')

@admin.register(DurationTour)
class DurationTourAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(SpecialOfferTour)
class SpecialOfferTourAdmin(admin.ModelAdmin):
    list_display = ('offer_type',)
    search_fields = ('offer_type', 'description')

# Дополнительные регистрации
admin.site.register(TourConditions)
admin.site.register(GalleryTour)
admin.site.register(AvailableDateTour)
admin.site.register(Order)