from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline

from reviews.models import Review
from .models import Restaurant, RestaurantImage


class ReviewInline(GenericTabularInline):
    model = Review


class ImageInline(TabularInline):
    model = RestaurantImage
    extra = 1


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, ImageInline]
    list_display = ("name", "region", "owner")
    search_fields = ("name", "region__name", "owner__username")


admin.site.register(Restaurant, RestaurantAdmin)
