from django.apps import AppConfig
from django.core.signals import request_finished


class DjangoManualConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_manual'

    def ready(self) -> None:
        # Подключение сигналов с декораторами
        # from . import signals

        # Обычное подключение сигналов
        # request_finished.connect(signals.my_callback)

        return super().ready()