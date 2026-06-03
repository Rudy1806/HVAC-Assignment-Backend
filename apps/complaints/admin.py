from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'source', 'priority', 'status', 'branch', 'created_at')
    list_filter = ('source', 'priority', 'status', 'branch')
    search_fields = ('title', 'description', 'customer__name')
    readonly_fields = ('created_at', 'updated_at')
