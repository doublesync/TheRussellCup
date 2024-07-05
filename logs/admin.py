# Python imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from logs.models import UpgradeLog, PaymentLog, ContractLog

# Register your models here.
admin.site.register(UpgradeLog, ModelAdmin)
admin.site.register(PaymentLog, ModelAdmin)
admin.site.register(ContractLog, ModelAdmin)