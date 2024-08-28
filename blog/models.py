from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    photo = models.ImageField(default=None, blank=True, null=True, verbose_name="Фото")
    content = models.TextField(verbose_name="Текст")               
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      
    published = models.BooleanField(default=False)  

    def __str__(self):
        return self.title
