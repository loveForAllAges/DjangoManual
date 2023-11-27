from django.apps import AppConfig


class DjangoManualConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_manual'
