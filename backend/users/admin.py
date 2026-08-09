from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff',
    )
    search_fields = ('email', 'username')
    ordering = ('id',)
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('Foodgram', {'fields': ('avatar',)}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            'Foodgram',
            {
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                )
            },
        ),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', 'created_at')
    search_fields = (
        'user__username',
        'user__email',
        'author__username',
        'author__email',
    )
    autocomplete_fields = ('user', 'author')
