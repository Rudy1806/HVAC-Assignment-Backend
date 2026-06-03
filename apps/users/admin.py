from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email_id',
        'full_name',
        'role',
        'tenant',
        'branch',
        'is_active',
        'is_staff',
        'date_joined',
    )
    search_fields = ('email_id', 'full_name', 'mobile_num')
    list_filter = ('role', 'is_active', 'is_staff', 'branch', 'tenant')
    readonly_fields = ('date_joined', 'updated_at')
