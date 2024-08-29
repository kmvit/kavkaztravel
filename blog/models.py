from django.db import models
from core.models import BaseContent

class Blog(BaseContent):
    """Класс для модели Blog."""
    title = models.CharField(max_length=200, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      
    published = models.BooleanField(default=False)  

    def __str__(self):
        return self.title
