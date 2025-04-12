from django.contrib import admin
from .models import TourOperator, Tour, GalleryTour, TagTour, AvailableDateTour, Order


class GalleryTourInline(admin.TabularInline):
    model = GalleryTour
    extra = 1
    verbose_name = "Фотография тура"
    verbose_name_plural = "Галерея тура"


class AvailableDateTourInline(admin.TabularInline):
    model = AvailableDateTour
    extra = 1
    fields = ("start_date", "end_date", "is_active")


@admin.register(TourOperator)
class TourOperatorAdmin(admin.ModelAdmin):
    list_display = ("license_number", "region", "owner")
    search_fields = ("license_number",)
    list_filter = ("region",)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("title", "guide", "region", "price", "created_at")
    list_filter = ("region", "tags")
    search_fields = ("title", "description")
    inlines = [GalleryTourInline, AvailableDateTourInline]
    filter_horizontal = ("tags",)


@admin.register(TagTour)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "tag_type")
    search_fields = ("name", "tag_type")


@admin.register(GalleryTour)
class GalleryTourAdmin(admin.ModelAdmin):
    list_display = ("tour", "image")


@admin.register(AvailableDateTour)
class AvailableDateTourAdmin(admin.ModelAdmin):
    list_display = ("tour", "start_date", "end_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("tour__title",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("tour", "username", "phone", "date", "size")
    list_filter = ("date",)
    search_fields = ("username", "phone", "email", "tour__title")
