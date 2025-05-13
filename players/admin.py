from django.contrib import admin
from unfold.admin import ModelAdmin

from players.models import Modification, Player


class PlayerAdmin(ModelAdmin):
    """
    Admin interface for Player model.
    """

    search_fields = ["first_name", "last_name"]
    autocomplete_fields = ["user", "team"]


admin.site.register(Player, PlayerAdmin)
admin.site.register(Modification, ModelAdmin)
