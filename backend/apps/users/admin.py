from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import SocialAccount, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "id",
        "username",
        "nickname",
        "email",
        "role",
        "status",
        "is_staff",
        "joined_at",
    )
    list_filter = (
        "role",
        "status",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    search_fields = (
        "username",
        "nickname",
        "email",
    )
    ordering = ("id",)
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "nickname",
                    "profile_image_url",
                    "role",
                    "status",
                    "joined_at",
                    "deleted_at",
                )
            },
        ),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "nickname",
                    "email",
                    "profile_image_url",
                    "role",
                    "status",
                )
            },
        ),
    )


@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "provider",
        "provider_user_id",
        "email",
        "created_at",
    )
    list_filter = ("provider",)
    search_fields = (
        "user__username",
        "user__nickname",
        "provider_user_id",
        "email",
    )
    ordering = ("id",)