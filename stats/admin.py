# Python imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from stats.models import Season, Playoff, PlayoffRound, PlayoffSeries
from stats.models import Game, PlayoffGame, TeamGameStats, PlayerGameStats

# Register your models here.
class SeasonAdmin(ModelAdmin):
    search_fields = ['season']
    ordering = ['-season']

class PlayoffAdmin(ModelAdmin):
    search_fields = ['season__season']
    autocomplete_fields = ['season', 'quarterfinals', 'semifinals', 'finals']
    ordering = ['-season__season']

class PlayoffRoundAdmin(ModelAdmin):
    search_fields = ['playoff__season__season', 'type']
    autocomplete_fields = ['playoff']
    ordering = ['-playoff__season__season']

class PlayoffSeriesAdmin(ModelAdmin):
    search_fields = ['team_a__name', 'team_b__name']
    autocomplete_fields = ['team_a', 'team_b', 'round']
    ordering = ['-round__playoff__season']

class GameAdmin(ModelAdmin):
    search_fields = ['week', 'home_team__name', 'away_team__name']
    autocomplete_fields = ['home_team', 'away_team']
    ordering = ['-season', '-week']    

class PlayoffGameAdmin(ModelAdmin):
    search_fields = ['week', 'home_team__name', 'away_team__name']
    autocomplete_fields = ['home_team', 'away_team', 'series']
    ordering = ['-season', '-week']

class TeamGameStatsAdmin(ModelAdmin):
    search_fields = ['team__city', 'team__name']
    autocomplete_fields = ['game', 'team']

class PlayerGameStatsStatsAdmin(ModelAdmin):
    search_fields = ['player__first_name', 'player__last_name']
    autocomplete_fields = ['game', 'player']

admin.site.register(Season, SeasonAdmin)
admin.site.register(Playoff, PlayoffAdmin)
admin.site.register(PlayoffRound, PlayoffRoundAdmin)
admin.site.register(PlayoffSeries, PlayoffSeriesAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(PlayoffGame, PlayoffGameAdmin)
admin.site.register(TeamGameStats, TeamGameStatsAdmin)
admin.site.register(PlayerGameStats, PlayerGameStatsStatsAdmin)
