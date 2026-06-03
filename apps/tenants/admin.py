from django.contrib import admin

from .models import Branch, Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_id', 'mobile_num', 'created_at')
    search_fields = ('name', 'email_id', 'mobile_num')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'email_id')
    search_fields = ('name', 'tenant__name', 'email_id')
