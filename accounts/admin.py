from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'can_pay_players', 'can_mark_upgrades', 'has_care_package', 'has_second_player_slot', 'sp', 'xp']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('can_pay_players', 'can_mark_upgrades', 'has_care_package', 'has_second_player_slot', 'sp', 'xp')}),
    )