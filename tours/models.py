from django.conf import settings
from django.db import models
from core.models import BaseContent
from regions.models import Region


class Guide(BaseContent):
    region = models.ForeignKey(Region, on_delete=models.CASCADE,
                               related_name='guides')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='guides')
    experience = models.IntegerField()  # Years of experience

    def __str__(self):
        return self.name


class TourOperator(BaseContent):
    region = models.ForeignKey(Region, on_delete=models.CASCADE,
                               related_name='touroperators')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='touroperators')
    license_number = models.CharField(max_length=100)

    def __str__(self):
        return self.name
