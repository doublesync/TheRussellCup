# Python imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from players.models import Player, Modification

# Register your models here.
class PlayerAdmin(ModelAdmin):
    search_fields = ['first_name', 'last_name']
    autocomplete_fields = ['user', 'team']

admin.site.register(Player, PlayerAdmin)
admin.site.register(Modification, ModelAdmin)