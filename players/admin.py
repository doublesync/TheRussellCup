# Python imports
from django.contrib import admin

# Local imports
from players.models import Player, Modification

# Register your models here.
admin.site.register(Player)
admin.site.register(Modification)
