from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(admin.ModelAdmin):
    ordering = ["first_name", "last_name", "email", "username"]
    model = User
    list_display = [
        "first_name",
        "last_name",
        "email",
        "username",
        "is_staff",
        "is_active",
        "is_superuser",
        "last_login",
        "created_at",
    ]
    list_filter = [
        "first_name",
        "last_name",
        "email",
        "username",
        "is_staff",
        "is_active",
    ]

    search_fields = ["first_name", "last_name", "email"]
    readonly_fields = ["created_at", "updated_at", "last_login"]


admin.site.register(User, UserAdmin)
