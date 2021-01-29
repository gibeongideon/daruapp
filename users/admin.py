from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class DuserAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'username', 'phone_number','email', 'first_name', 'last_name',
        'my_code', 'daru_code', 'last_login', 'active')

    list_display_links = ('id',)
    search_fields = ('id',)
    ordering = ('id',)
    readonly_fields = ('password',)


admin.site.register(User, DuserAdmin)
