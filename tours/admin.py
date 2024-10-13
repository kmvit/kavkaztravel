from django.contrib import admin
from .models import DateTour, EstimationTour, GalleryTour, Geo, Guide, Order, Tag, Tour, TourOperator

admin.site.register(Guide)
admin.site.register(TourOperator)
admin.site.register(Tour)
admin.site.register(GalleryTour)
admin.site.register(DateTour)
admin.site.register(Tag)
admin.site.register(EstimationTour)
admin.site.register(Order)
admin.site.register(Geo)
