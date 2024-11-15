from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseContent(models.Model):
    """Базовый класс для моделей."""

    name = models.CharField(max_length=100)
    url = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="content_images/", blank=True, null=True)
    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
