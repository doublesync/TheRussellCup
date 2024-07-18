# Python imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from stats.models import Season, Game, TeamGameStats, PlayerGameStats

# Register your models here.
class GameAdmin(ModelAdmin):
    search_fields = ['week', 'home_team__name', 'away_team__name']
    autocomplete_fields = ['home_team', 'away_team']
    ordering = ['-season', '-week']    

class TeamGameStatsAdmin(ModelAdmin):
    search_fields = ['team__city', 'team__name']
    autocomplete_fields = ['game', 'team']

class PlayerGameStatsStatsAdmin(ModelAdmin):
    search_fields = ['player__first_name', 'player__last_name']
    autocomplete_fields = ['game', 'player']

admin.site.register(Season, ModelAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(TeamGameStats, TeamGameStatsAdmin)
admin.site.register(PlayerGameStats, PlayerGameStatsStatsAdmin)
