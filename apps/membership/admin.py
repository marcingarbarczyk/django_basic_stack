from django.contrib import admin

from apps.membership.models import LoginAttempt, User
from apps.utils.admin import SearchableRelatedFieldListFilter


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'created_at',
        'updated_at',
    )
    date_hierarchy = 'created_at'
    search_fields = (
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'is_active',
        'is_staff',
        'created_at',
    )
    ordering = ('id',)


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'username', 'user', 'ip', 'city', 'has_logged_in']
    list_filter = [
        ('user', SearchableRelatedFieldListFilter),
        'has_logged_in',
    ]
    search_fields = [
        'username',
        'browser',
        'ip',
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    fields = [
        'user',
        'username',
        ('attempted_at', 'has_logged_in'),
        'browser',
        'ip',
        'geolocation',
        ('created_at', 'updated_at'),
    ]
    readonly_fields = [
        'ip',
        'user',
        'username',
        'attempted_at',
        'has_logged_in',
        'browser',
        'geolocation',
        'created_at',
        'updated_at',
    ]
