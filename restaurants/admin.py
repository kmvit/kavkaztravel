from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Restaurant, RestaurantImage


class ImageInline(TabularInline):
    model = RestaurantImage
    extra = 1


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ("name", "region", "owner")
    search_fields = ("name", "region__name", "owner__username")


admin.site.register(Restaurant, RestaurantAdmin)
