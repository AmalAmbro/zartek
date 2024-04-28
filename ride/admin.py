from django.contrib import admin
from ride.models import *
from django.contrib.auth.admin import UserAdmin

class UserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""

    fieldsets = None
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'is_staff', 'is_driver')
    search_fields = ('username',)
    ordering = ('-id',)

# Register your models here.
admin.site.register(Rides)
admin.site.register(User, UserAdmin)

