# Python imports
from django.contrib import admin

# Local imports
from logs.models import UpgradeLog, PaymentLog

# Register your models here.
admin.site.register(UpgradeLog)
admin.site.register(PaymentLog)