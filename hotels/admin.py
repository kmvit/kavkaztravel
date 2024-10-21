from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline

from reviews.models import Review
from .models import Hotel, Tag, HotelImage


class ReviewInline(GenericTabularInline):
    model = Review


class ImageInline(TabularInline):
    model = HotelImage
    extra = 1


class HotelAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, ImageInline]
    list_display = ("name", "region", "owner")
    search_fields = ("name", "region__name", "owner__username")


admin.site.register(Hotel, HotelAdmin)
admin.site.register(Tag)
