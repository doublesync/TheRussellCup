# Python imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from stats.models import Season, Game, TeamGameStats, PlayerGameStats

# Register your models here.
class GameAdmin(ModelAdmin):
    search_fields = ['season', 'week', 'home_team', 'away_team']
    autocomplete_fields = ['home_team', 'away_team']
    ordering = ['-season', '-week']    

class TeamGameStatsAdmin(ModelAdmin):
    autocomplete_fields = ['game']

class PlayerGameStatsStatsAdmin(ModelAdmin):
    autocomplete_fields = ['game', 'player']

admin.site.register(Season, ModelAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(TeamGameStats, TeamGameStatsAdmin)
admin.site.register(PlayerGameStats, PlayerGameStatsStatsAdmin)
