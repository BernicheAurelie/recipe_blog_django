from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import User
from django.contrib.auth import get_user_model
from .forms import CreerUtilisateur, ModifierUtilisateur


class UserAdmin(AuthUserAdmin):
    add_form = CreerUtilisateur
    form = ModifierUtilisateur
    model = User
    # model = get_user_model()


admin.site.register(User, UserAdmin)