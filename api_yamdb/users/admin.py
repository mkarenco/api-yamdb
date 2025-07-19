from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_active'
    )
    list_editable = (
        'email',
        'role'
    )
    search_fields = (
        'username',
        'email'
    )
    list_filter = (
        'role',
        'is_active',
        'is_staff'
    )
    ordering = (
        'username',
    )
