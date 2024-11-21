from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import Restaurant, RestaurantImage, ReviewImageRestaurant, ReviewRestaurant


class ImageInline(TabularInline):
    model = RestaurantImage
    extra = 1


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "owner")
    search_fields = ("name", "region__name", "owner__username")

class ReviewRestauranAdmin(admin.ModelAdmin):
    pass

class ReviewImageRestaurantlAdmin(admin.ModelAdmin):
    pass

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(ReviewRestaurant, ReviewRestauranAdmin)

admin.site.register(ReviewImageRestaurant, ReviewImageRestaurantlAdmin)