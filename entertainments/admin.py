from django.contrib import admin
from .models import Entertainment, ReviewEntertainment, ReviewImageEntertainment


class EntertainmentAdmin(admin.ModelAdmin):
    list_display = ("name", "region")
    search_fields = ("name", "region__name")

class ReviewEntertainmentAdmin(admin.ModelAdmin):
    pass

class ReviewImageEntertainmentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Entertainment, EntertainmentAdmin)
admin.site.register(ReviewEntertainment, ReviewEntertainmentAdmin)
admin.site.register(ReviewImageEntertainment, ReviewImageEntertainmentAdmin)
