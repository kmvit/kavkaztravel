from django.contrib import admin
from .models import Brand, Model, Year, Color, BodyType, Auto, Foto, Company

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class ModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class YearAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class BodyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

class AutoAdmin(admin.ModelAdmin):
    pass

class FotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'auto')
    search_fields = ('auto__model__name',)
    list_filter = ('auto',)
    ordering = ('auto',)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'working_hours', 'owner')
    search_fields = ('name', 'working_hours', 'owner__username')
    list_filter = ('owner',)
    ordering = ('name',)

# Register your models here.
admin.site.register(Brand, BrandAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(BodyType, BodyTypeAdmin)
admin.site.register(Auto, AutoAdmin)
admin.site.register(Foto, FotoAdmin)
admin.site.register(Company, CompanyAdmin)

