from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        (
            "Credentials",
            {
                "fields": ("username", "password"),
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "birthdate",
                    "bio",
                    "is_critic",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
        (
            "Dates",
            {
                "fields": ("last_login", "date_joined"),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
