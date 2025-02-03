import os
from celery import Celery

# Указываем Django, где находится файл настроек
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создаем экземпляр Celery
app = Celery("config")

# Загружаем настройки из Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находим и регистрируем задачи в приложениях Django
app.autodiscover_tasks()
