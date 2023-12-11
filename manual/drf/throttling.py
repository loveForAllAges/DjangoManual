from django.core.cache import caches

from rest_framework.throttling import (
    AnonRateThrottle, ScopedRateThrottle, SimpleRateThrottle, UserRateThrottle,
    BaseThrottle
)

import random


# Использование кэша, отличного от 'default'.
class CustomAnonRateThrottle(AnonRateThrottle):
    # cache = caches['alternate']
    rate = '1/minute'


class CustomUserRateThrottle(UserRateThrottle):
    rate = '1/hour'


class CustomScopedRateThrottle(ScopedRateThrottle):
    rate = '1/second'


# Тротлинг, если рандомное число не 1
class RandomRateThrottle(BaseThrottle):
    def allow_request(self, request, view):
        return random.randint(1, 10) != 1
