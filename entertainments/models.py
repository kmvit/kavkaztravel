from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from core.models import BaseContent
from Kavkaztome import settings
from regions.models import Region


class Entertainment(BaseContent):
    """Модель для представления развлекательных объектов.

    Эта модель описывает развлекательные объекты, включая адрес, 
    регион и владельца. Также поддерживается связь с рецензиями и 
    возможностью получения изображений, связанных с объектом.
    Методы:
        __str__(): Возвращает имя объекта.
        calculate_rating(): Вычисляет средний рейтинг на основе 
            связанных рецензий.
    """
    
    address = models.CharField(max_length=300)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="entertainments"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )

    class Meta:
        verbose_name = "Достопримечательность"
        verbose_name_plural = "Достопримечательности"

    def __str__(self):
        return self.name

    

class EntertainmentImage(models.Model):
    """ Модель для хранения изображений развлекательных объектов.

    Эта модель связывает изображения с конкретными развлекательными 
    объектами, позволяя хранить множественные изображения для каждого 
    объекта.
    
    Методы:
        __str__(): Возвращает идентификатор развлекательного объекта, 
            к которому принадлежит изображение.
    """
    entertainment = models.ForeignKey(
        Entertainment, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField()

    def __str__(self):
        return self.entertainment.id
