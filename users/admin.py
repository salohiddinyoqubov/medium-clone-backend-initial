from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Recommendation


@admin.register(CustomUser)  # administrator panelida ro'yxatdan o'tdan o'tkazish
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {
                "fields": (
                    "middle_name",
                    "avatar",
                )
            },
        ),
    )
    list_display = ("id", "username", "email", "first_name", "last_name", "middle_name")
    list_display_links = ("id", "username", "email")
    search_fields = ("username", "email", "first_name", "last_name", "middle_name")
    list_filter = ("last_login", "date_joined", "is_staff", "is_superuser", "is_active")


admin.site.register(Recommendation)
