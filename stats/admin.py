# Python imports
from django.contrib import admin

# Local imports
from stats.models import Game, TeamGameStats, PlayerGameStats

# Register your models here.
admin.site.register(Game)
admin.site.register(TeamGameStats)
admin.site.register(PlayerGameStats)
