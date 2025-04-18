from django.contrib import admin
from unfold.admin import ModelAdmin

from logs.models import ContractLog, ContractOfferLog, PaymentLog, TrophyLog, UpgradeLog


class TransactionMoveLogAdmin(ModelAdmin):
    """
    Admin for the TransactionMoveLog model.
    """

    exclude = ["approved"]
    search_fields = ["team", "signed", "released"]
    autocomplete_fields = ["team", "signed", "released"]


class LogAdmin(ModelAdmin):
    """
    Admin for the Log models.
    """

    search_fields = ["player__first_name", "player__last_name"]
    autocomplete_fields = ["player"]


admin.site.register(UpgradeLog, LogAdmin)
admin.site.register(PaymentLog, LogAdmin)
admin.site.register(ContractLog, LogAdmin)
admin.site.register(ContractOfferLog, LogAdmin)
admin.site.register(TrophyLog, LogAdmin)
