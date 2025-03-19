# reviews/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import CarReview, CarReviewImage, CarRating


class CarReviewImageInline(admin.TabularInline):
    model = CarReviewImage
    extra = 1


class CarRatingInline(admin.TabularInline):
    model = CarRating
    extra = 5


@admin.register(CarReview)
class CarReviewAdmin(admin.ModelAdmin):
    """Админка для отзывов с модерацией"""

    list_display = ("user", "car", "created_at", "is_approved") 
    list_filter = ("is_approved", "created_at")
    search_fields = ("user__username", "car__make", "car__model")
    actions = ["approve_reviews"]
    inlines = [CarReviewImageInline, CarRatingInline]

    list_editable = ("is_approved",)

    @admin.action(description="Одобрить выбранные отзывы")
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)


@admin.register(CarReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ("review_link", "image_preview")  # Используем метод для отображения ссылки на отзыв

    def review_link(self, obj):
        # Возвращаем ссылку на отзыв
        return format_html('<a href="{}">{}</a>', reverse("admin:reviews_carreview_change", args=[obj.review.id]), obj.review)
    review_link.short_description = "Review"  # Заголовок столбца

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>', obj.image.url
            )
        return "Нет изображения"

    image_preview.short_description = "Превью"


@admin.register(CarRating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("review_link", "criteria", "score")  # Используем метод для отображения ссылки на отзыв

    def review_link(self, obj):
        # Возвращаем ссылку на отзыв
        return format_html('<a href="{}">{}</a>', reverse("admin:reviews_carreview_change", args=[obj.review.id]), obj.review)
    review_link.short_description = "Review"  # Заголовок столбца

    list_filter = ("criteria",)
    search_fields = (
        "review__user__username",
        "review__car__make",
        "review__car__model",
    )
