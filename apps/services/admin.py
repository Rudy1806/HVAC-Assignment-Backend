from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'price', 'gst_percent', 'tenant')
    list_filter = ('tenant',)
    search_fields = ('name',)
