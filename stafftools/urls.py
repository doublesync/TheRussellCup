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
    path("refreshstats/", views.RefreshStatsView.as_view(), name="refresh_stats"),
    path("paymentrequest/", views.PaymentRequestView.as_view(), name="payment_request"),
    path("paymentrequests/", views.PaymentRequestsView.as_view(), name="payment_requests"),
    path("offercontracts/", views.OfferContractsView.as_view(), name="offer_contracts"),
    path("viewoffers/", views.ViewOffersView.as_view(), name="view_offers"),
    path("viewplayeroffers/", views.ViewPlayerOffersView.as_view(), name="view_player_offers"),
    path("withdrawoffers/<str:return_type>/", views.htmx_withdraw_offers, name="htmx_withdraw_offers"),
    path("acceptoffer/<int:offer_id>/", views.htmx_accept_offer, name="htmx_accept_offer"),
    # fmt:on
]
