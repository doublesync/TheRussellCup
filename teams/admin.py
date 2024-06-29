# Django imports
from django.contrib import admin

# Local imports
from teams.models import Team, Draft, DraftPick, DraftOrder

# Register your models here.
admin.site.register(Team)
admin.site.register(Draft)
admin.site.register(DraftPick)
admin.site.register(DraftOrder)