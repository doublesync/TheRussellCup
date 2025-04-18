from django.contrib import admin
from unfold.admin import ModelAdmin

from events.models import Entree, Event

admin.site.register(Event, ModelAdmin)
admin.site.register(Entree, ModelAdmin)
