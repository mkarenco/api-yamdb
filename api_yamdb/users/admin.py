from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'bio',
        'is_active'
    )
    list_editable = (
        'role',
        'email ',
        'last_name',
    )
    search_fields = (
        'username',
        'first_name'
    )
    list_filter = (
        'role',
        'is_active',
        'is_staff'
    )
    ordering = ('username',)
