from django.contrib import admin
from .models import Invoice, InvoiceItem

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_amount', 'status', 'tenant')
    list_filter = ('status', 'tenant')
    search_fields = ('customer__name',)

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'service', 'description', 'quantity', 'price')
