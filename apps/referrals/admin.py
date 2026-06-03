from django.contrib import admin
from .models import ReferralCode

@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'generated_by', 'is_active', 'tenant')
    list_filter = ('is_active', 'tenant')
    search_fields = ('code',)
