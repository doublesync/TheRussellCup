# Python imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from teams.models import Team
from players.models import Player
from logs.models import UpgradeLog, PaymentLog, ContractLog, TransactionMoveLog

class TransactionMoveLogAdmin(ModelAdmin):
    exclude = ['approved']
    search_fields = ['team', 'signed', 'released']
    autocomplete_fields = ['team', 'signed', 'released']

class LogAdmin(ModelAdmin):
    search_fields = ['player__first_name', 'player__last_name']
    autocomplete_fields = ['player']

# Register your models here.
admin.site.register(UpgradeLog, LogAdmin)
admin.site.register(PaymentLog, LogAdmin)
admin.site.register(ContractLog, LogAdmin)
admin.site.register(TransactionMoveLog, TransactionMoveLogAdmin)