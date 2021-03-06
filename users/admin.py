from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class DuserAdmin(UserAdmin):

    list_display = (
        "id",
        "username",
        "phone_number",
        "email",
        "first_name",
        "last_name",
        "code",
        "referer_code",
        "last_login",
        "active",
    )

    list_display_links = ("id",)
    search_fields = ("id",)
    ordering = ("id",)

    list_editable = (
        "phone_number",
        "code",
        "referer_code",
    )
    readonly_fields = ("password",)


admin.site.register(User, DuserAdmin)
