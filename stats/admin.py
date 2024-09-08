# Python imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from stats.models import Season, Playoff, PlayoffRound, PlayoffSeries
from stats.models import Game, PlayoffGame, TeamGameStats, PlayerGameStats, PlayerSeasonStats, TeamSeasonStats

# Register your models here.
class SeasonAdmin(ModelAdmin):
    search_fields = ['season']
    ordering = ['-season']
    exclude = [
        "highest_points", "highest_rebounds", "highest_assists", "highest_steals", "highest_blocks", "highest_turnovers",
        "highest_field_goals_made", "highest_field_goals_attempted", "highest_three_pointers_made", "highest_three_pointers_attempted",
        "highest_free_throws_made", "highest_free_throws_attempted", "highest_offensive_rebounds", "highest_personal_fouls",
        "highest_plus_minus", "highest_points_responsible_for", "highest_dunks", "highest_defensive_rebounds", "highest_game_score",
        "highest_effective_field_goal_percentage", "highest_true_shooting_percentage", "highest_turnover_percentage"
    ]

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

# Inlines for the GameAdmin and PlayoffGameAdmin classes
class TeamGameStatsInline(admin.TabularInline):
    search_fields = ['team__city', 'team__name']
    autocomplete_fields = ['game', 'team']
    model = TeamGameStats
    show_change_link = True

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            user_created_forms = obj.playergamestats_set.count()
            return max(2 - user_created_forms, 0)
        return 2

class PlayerGameStatsInline(admin.TabularInline):
    search_fields = ['player__first_name', 'player__last_name']
    autocomplete_fields = ['game', 'player']
    model = PlayerGameStats
    show_change_link = True

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            user_created_forms = obj.playergamestats_set.count()
            return max(10 - user_created_forms, 0)
        return 10

class GameAdmin(ModelAdmin):
    search_fields = ['week', 'home_team__name', 'away_team__name']
    autocomplete_fields = ['home_team', 'away_team']
    ordering = ['-season', '-week']   
    inlines = [TeamGameStatsInline, PlayerGameStatsInline] 

class PlayoffGameAdmin(ModelAdmin):
    search_fields = ['week', 'home_team__name', 'away_team__name']
    autocomplete_fields = ['home_team', 'away_team', 'series']
    ordering = ['-season', '-week']
    inlines = [TeamGameStatsInline, PlayerGameStatsInline]

class TeamGameStatsAdmin(ModelAdmin):
    search_fields = ['team__city', 'team__name']
    autocomplete_fields = ['game', 'team']
    ordering = ['-game__season', '-game__week']

class PlayerGameStatsStatsAdmin(ModelAdmin):
    search_fields = ['player__first_name', 'player__last_name']
    autocomplete_fields = ['game', 'player']
    ordering = ['-game__season', '-game__week']

class PlayerSeasonStatsAdmin(ModelAdmin):
    search_fields = ['player__first_name', 'player__last_name']
    autocomplete_fields = ['season', 'player']
    ordering = ['-season']

class TeamSeasonStatsAdmin(ModelAdmin):
    search_fields = ['team__city', 'team__name']
    autocomplete_fields = ['season', 'team']
    ordering = ['-season']

admin.site.register(Season, SeasonAdmin)
admin.site.register(Playoff, PlayoffAdmin)
admin.site.register(PlayoffRound, PlayoffRoundAdmin)
admin.site.register(PlayoffSeries, PlayoffSeriesAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(PlayoffGame, PlayoffGameAdmin)
admin.site.register(TeamGameStats, TeamGameStatsAdmin)
admin.site.register(PlayerGameStats, PlayerGameStatsStatsAdmin)
admin.site.register(PlayerSeasonStats, PlayerSeasonStatsAdmin)
admin.site.register(TeamSeasonStats, TeamSeasonStatsAdmin)