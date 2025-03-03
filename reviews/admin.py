from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from .models import Review, ReviewImage, Rating


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 1


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 5


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для отзывов с модерацией"""

    list_display = ("user", "car", "created_at", "is_approved") 
    list_filter = ("is_approved", "created_at")
    search_fields = ("user__username", "car__make", "car__model")
    actions = ["approve_reviews"]
    inlines = [ReviewImageInline, RatingInline]

    list_editable = ("is_approved",)  # ✅ Галочка прямо в списке!

    @admin.action(description="Одобрить выбранные отзывы")
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ("review", "image_preview")

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>', obj.image.url
            )
        return "Нет изображения"

    image_preview.short_description = "Превью"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("review", "criteria", "score")
    list_filter = ("criteria",)
    search_fields = (
        "review__user__username",
        "review__car__make",
        "review__car__model",
    )
