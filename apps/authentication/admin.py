from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'tenant', 'email_id')
    list_filter = ('role', 'tenant')
    search_fields = ('username', 'email_id')
