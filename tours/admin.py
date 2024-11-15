from django.contrib import admin
from .models import (
    DateTour,
    GalleryTour,
    Geo,
    Guide,
    Order,
    ReviewTour,
    Tag,
    Tour,
    TourOperator,
)

admin.site.register(Guide)
admin.site.register(TourOperator)
admin.site.register(Tour)
admin.site.register(GalleryTour)
admin.site.register(DateTour)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(Geo)
admin.site.register(ReviewTour)
