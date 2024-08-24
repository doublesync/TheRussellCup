# Django imports
from django.contrib.auth.decorators import login_required
from django.urls import path

# Local imports
from stafftools import views

# Create your urls here.
urlpatterns = [
    # fmt:off
    path("payuser/<int:id>/<str:payment_type>/", views.pay_user, name="pay_user"),
    path("payautocollections/", views.pay_auto_collections, name="pay_auto_collections"),
    path("bulkpay/", views.BulkPayView.as_view(), name="bulk_pay"),
    path("bulkassignteam/", views.BulkAssignTeamView.as_view(), name="bulk_assign_team"),
    # fmt:on
]
