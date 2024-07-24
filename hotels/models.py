from datetime import date
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from Kavkaztome import settings
from core.models import BaseContent
from regions.models import Region
from reviews.models import Review


class Tag(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='tag_icons/')

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class AccommodationType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Hotel(BaseContent):
    address = models.CharField(max_length=300)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,
                               related_name='hotels')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='hotels')
    tags = models.ManyToManyField(Tag, related_name='hotels')
    reviews = GenericRelation(Review, related_query_name='reviews')

    class Meta:
        verbose_name = 'Гостиница'
        verbose_name_plural = 'Гостиницы'

    def __str__(self):
        return self.name

    def calculate_rating(self):
        reviews = self.reviews.all()
        total_rating = sum(review.rating for review in reviews)
        return total_rating / reviews.count() if reviews.exists() else 0


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='images',
                              on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.hotel.id


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='rooms',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"


class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name='images',
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/')

    def __str__(self):
        return f"Image for {self.room.name}"


class RoomPrice(models.Model):
    SEASONS = (
        ('low', 'Low Season'),
        ('high', 'High Season'),
        ('holiday', 'Holiday Season'),
    )
    room = models.ForeignKey(Room, related_name='prices',
                             on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    season = models.CharField(max_length=10, choices=SEASONS, default='low')

    class Meta:
        unique_together = ('room', 'date')

    def __str__(self):
        return f"{self.room.name} - {self.date}: {self.price}"

    @property
    def is_high_season(self):
        today = date.today()
        return self.season == 'high' or (
                self.season == 'holiday' and today.month in [12, 1])

    @property
    def is_low_season(self):
        today = date.today()
        return self.season == 'low' or (
                self.season == 'holiday' and today.month not in [12, 1])
