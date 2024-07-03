# Python imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from logs.models import UpgradeLog, PaymentLog

# Register your models here.
@admin.register(UpgradeLog)
class UpgradeLogAdmin(ModelAdmin):
    pass

@admin.register(PaymentLog)
class PaymentLogAdmin(ModelAdmin):
    pass