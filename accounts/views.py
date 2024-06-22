# Django imports
from django.shortcuts import render
from django.shortcuts import get_object_or_404

# Local imports
from accounts.models import CustomUser


# Create your views here.
def user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    return render(request, "account/user.html", {"user": user})
