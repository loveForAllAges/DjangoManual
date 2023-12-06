"""
Раздел: Signals (Сигналы).


Сигналы позволяют определнным отправителям уведомить группу получателей о том, 
что произошло какое-то действие.

Чтобы получить сигнал, зарегистрируйте функцию приемника, используя Signal.connect().

Signal.connect(
    receiver, # функиця обратного вызова, которая будет подключена к сигналу.
    sender=None, # указывает конкретного отправителя, от которого принимаются сигналы.
    weak=True,  # False, если приемник является локальной функцией.
    dispatch_uid=None # id получателя сигнала.
)


Отправка сигналов:
Signal.send(sender, **kwargs)
Signal.send_robust(sender, **kwargs)
Signal.asend(sender, **kwargs)
Signal.asend_robust(sender, **kwargs)


Отключение сигналов:
Signal.disconnect(receiver=None, sender=None, dispatch_uid=None)
"""


def my_callback(sender, **kwargs):
    # Фукнция приемник.
    print('Request finished!')


# import asyncio
# async def my_callback(sender, **kwargs):
#     # Асинхронная функция приемник.
#     await asyncio.sleep(5)
#     print('Request finished!')


from django.core.signals import request_finished
# Подключение функций приемника

# 1.
# request_finished.connect(my_callback)

# 2.
from django.dispatch import receiver
# @receiver(request_finished)
# def my_callback(sender, **kwargs):
#     print('OKOKOKOK')

from django.db.models.signals import pre_save
from .models import Author

@receiver(pre_save, sender=Author)
def my_handler(sender, **kwargs):
    # Сигнал отправленный до сохранения модели.
    # Фукнция вызывается только при Author сохранении экземпляра.
    pass


# Для предотвращения дублирования сигналов, необходимо передать dispatch_uid.
request_finished.connect(my_callback, dispatch_uid='my_unique_identifier')


# Все сигналы являются экземплярами Signal.
import django.dispatch

pizza_done = django.dispatch.Signal()


class PizzaStore:
    def send_pizza(self, toppings, size):
        pizza_done.send(sender=self.__class__, toppings=toppings, size=size)

    async def asend_pizza(self, toppings, size):
        await pizza_done.asend(sender=self.__class__, toppings=toppings, size=size)

