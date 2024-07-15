# Django imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from teams.models import Team, Draft, DraftPick, DraftOrder

# Register your models here.
class TeamAdmin(ModelAdmin):
    search_fields = ['name', 'city']
    list_display = ['name', 'city', 'manager']

class DraftPickAdmin(ModelAdmin):
    autocomplete_fields = ['player']

admin.site.register(Team, TeamAdmin)
admin.site.register(Draft, ModelAdmin)
admin.site.register(DraftPick, DraftPickAdmin)
admin.site.register(DraftOrder, ModelAdmin)