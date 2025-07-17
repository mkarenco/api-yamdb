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
        'is_staff',
        'is_active'
    )
    list_editable = (
        'first_name',
        'last_name',
        'email',
        'bio',
        'role'
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email'
    )
    list_filter = (
        'role',
        'is_active',
        'is_staff'
    )
    ordering = (
        'username',
        'last_name'
    )
