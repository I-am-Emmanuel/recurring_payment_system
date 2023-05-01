from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'first_name', 'last_name', ),
            },
        ),
    )
