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

    list_display = (
        "user",
        "car",
        "score",
        "average_rating",
        "created_at",
        "is_approved",
    )
    list_filter = ("is_approved", "created_at", "score")
    search_fields = ("user__username", "car__make", "car__model")
    actions = ["approve_reviews"]
    inlines = [CarReviewImageInline, CarRatingInline]
    list_editable = ("is_approved",)

    readonly_fields = ("created_at",)
    save_on_top = True
    ordering = ("-created_at",)

    def average_rating(self, obj):
        return obj.get_average_rating(obj.car)

    average_rating.short_description = "Средний рейтинг"

    @admin.action(description="Одобрить выбранные отзывы")
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)


@admin.register(CarReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = (
        "review_link",
        "image_preview",
    )

    def review_link(self, obj):
        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:reviews_carreview_change", args=[obj.car_review.id]),
            obj.car_review,
        )

    review_link.short_description = "Review"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px;"/>', obj.image.url
            )
        return "Нет изображения"

    image_preview.short_description = "Превью"


@admin.register(CarRating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "review_link",
        "criteria",
        "score",
    )

    def review_link(self, obj):

        return format_html(
            '<a href="{}">{}</a>',
            reverse("admin:reviews_carreview_change", args=[obj.car_review.id]),
            obj.car_review,
        )

    review_link.short_description = "Review"

    list_filter = ("criteria",)
    search_fields = (
        "car_review__user__username",
        "car_review__car__make",
        "car_review__car__model",
    )
