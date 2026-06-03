from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_num', 'lead_source', 'status', 'tenant')
    list_filter = ('lead_source', 'status', 'tenant')
    search_fields = ('name', 'mobile_num', 'email_id')
