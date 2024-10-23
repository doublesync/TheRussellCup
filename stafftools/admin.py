# Python imports
from django.contrib import admin
from unfold.admin import ModelAdmin

# Local imports
from stafftools.models import PaymentRequest

# Register your models here.
admin.site.register(PaymentRequest, ModelAdmin)