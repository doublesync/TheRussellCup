# Python imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from events.models import Event, Entree

admin.site.register(Event, ModelAdmin)
admin.site.register(Entree, ModelAdmin)