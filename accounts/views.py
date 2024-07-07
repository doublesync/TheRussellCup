# Django imports
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Local imports
from accounts.models import CustomUser
from simulation import payment as payment


# Create your views here.
def user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    return render(request, "account/user.html", {"user": user})

# This is a function based view that will give contract payments to a user's players
def claim_contracts(request):
    user = request.user
    payments = payment.pay_contracts(user)
    return HttpResponse(payments)