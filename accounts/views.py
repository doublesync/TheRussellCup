from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from accounts.models import CustomUser
from simulation import payment


def user(request, user_id):
    """
    View function to display user profile.
    """

    return render(
        request,
        "account/user.html",
        {"user": get_object_or_404(CustomUser, id=user_id)},
    )


def claim_contracts(request):
    """
    View function to claim contracts for the logged-in user.
    """

    return HttpResponse(payment.pay_contracts(request.user))
