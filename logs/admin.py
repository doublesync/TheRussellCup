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

# Register your models here.
admin.site.register(UpgradeLog, ModelAdmin)
admin.site.register(PaymentLog, ModelAdmin)
admin.site.register(ContractLog, ModelAdmin)
admin.site.register(TransactionMoveLog, TransactionMoveLogAdmin)