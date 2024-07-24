from django.contrib import admin
from .models import Entertainment


class EntertainmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('name', 'region__name')


admin.site.register(Entertainment, EntertainmentAdmin)
