from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.contenttypes.admin import GenericTabularInline


from .models import Hotel, ReviewHotel, ReviewImageHotel, Tag, HotelImage


class ImageInline(TabularInline):
    model = HotelImage
    extra = 1


class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "owner")
    search_fields = ("name", "region__name", "owner__username")

class ReviewHotelAdmin(admin.ModelAdmin):
    pass

class ReviewImageHotelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Hotel, HotelAdmin)
admin.site.register(Tag)
admin.site.register(ReviewHotel, ReviewHotelAdmin)
admin.site.register(ReviewImageHotel, ReviewImageHotelAdmin)