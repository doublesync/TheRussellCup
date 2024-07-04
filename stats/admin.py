# Python imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from stats.models import Season, Game, TeamGameStats, PlayerGameStats

# Register your models here.
class PlayerGameStatsStatsAdmin(ModelAdmin):
    autocomplete_fields = ['player']

admin.site.register(Season, ModelAdmin)
admin.site.register(Game, ModelAdmin)
admin.site.register(TeamGameStats, ModelAdmin)
admin.site.register(PlayerGameStats, PlayerGameStatsStatsAdmin)
