# Python imports
import hashlib

# Django imports
from django.db import models
from django.core.cache import cache

# Create your managers here.
class CachedManager(models.Manager):
    def from_cache(self, filterdict, model_name):
        cachekey = f'{model_name}Cache' + hashlib.md5(str(filterdict).encode()).hexdigest()
        res = cache.get(cachekey)
        if res:
            return res  # Return only the queryset from cache
        else:
            res = self.filter(**filterdict)
            cache.set(cachekey, res, 300)  # Cache for five minutes
            return res

class GameManager(CachedManager):
    def from_cache(self, filterdict):
        return super().from_cache(filterdict, 'Game')

class TeamGameStatsManager(CachedManager):
    def from_cache(self, filterdict):
        return super().from_cache(filterdict, 'TeamGameStats')

class PlayerGameStatsManager(CachedManager):
    def from_cache(self, filterdict):
        return super().from_cache(filterdict, 'PlayerGameStats')