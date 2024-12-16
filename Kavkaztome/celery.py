# your_project/celery.py
import os
from celery import Celery

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kavkaztome.settings')

# Создаём приложение Celery
app = Celery('Kavkaztome')

# Настройка Celery для использования настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи в ваших приложениях Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

