# Django imports
from django.shortcuts import render

# Local imports
from accounts.models import CustomUser


# Create your views here.
def user(request, pk):
    user_exists = CustomUser.objects.filter(pk=pk).exists()
    if user_exists:
        return render(
            request, "account/user.html", {"user": CustomUser.objects.get(pk=pk)}
        )
    else:
        return render(request, "500.html", {"error": "User does not exist"})
