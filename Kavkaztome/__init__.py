# your_project/__init__.py

from __future__ import absolute_import, unicode_literals

# Импортируем Celery, чтобы он был доступен на старте проекта
from .celery import app as celery_app

__all__ = ('celery_app',)
