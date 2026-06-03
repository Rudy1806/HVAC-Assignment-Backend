from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile_num', 'branch', 'customer_type', 'created_at')
    list_filter = ('customer_type', 'branch')
    search_fields = ('name', 'mobile_num', 'email_id')
    readonly_fields = ('created_at', 'updated_at')
