from django.contrib import admin
from .models import Quotation, QuotationItem

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'total_amount', 'status', 'tenant')
    list_filter = ('status', 'tenant')

@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ('quotation', 'service', 'quantity', 'price')
