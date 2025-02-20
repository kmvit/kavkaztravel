from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from core.models import BaseContent
from Kavkaztome import settings


class Region(BaseContent):
    """
    Класс, представляющий регион или город.
    """

    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )

    class Meta:
        verbose_name = "Регион/город"
        verbose_name_plural = "Регионы/города"

    def __str__(self):
        """Возвращает название региона."""
        return self.name


class RegionImage(models.Model):
    """
    Класс, представляющий изображение региона.
    """

    region = models.ForeignKey(Region, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        """Возвращает идентификатор региона, к которому относится изображение."""
        return str(self.region.id)
