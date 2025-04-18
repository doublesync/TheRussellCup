from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form that uses the CustomUser model.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "email",
            "username",
            "can_pay_players",
            "can_mark_upgrades",
            "has_care_package",
        )


class CustomUserChangeForm(UserChangeForm):
    """
    A custom user change form that uses the CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "username",
            "can_pay_players",
            "can_mark_upgrades",
            "has_care_package",
        )
