from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import forms
from . import models


class CustomUserAdmin(UserAdmin):
    add_form = forms.CustomUserCreationForm
    form = forms.CustomUserChangeForm
    list_display = ['email', 'username', 'age']
    model = models.CustomUser


admin.site.register(models.CustomUser, CustomUserAdmin)
