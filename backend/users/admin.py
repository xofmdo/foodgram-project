from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import User


@register(User)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',
    )
    fields = (
        'username', 'email', 'first_name', 'last_name',
    )
    search_fields = (
        'username', 'email',
    )
    list_filter = (
        'first_name', 'email',
    )
