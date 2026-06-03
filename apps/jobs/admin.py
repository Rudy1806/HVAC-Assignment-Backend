from django.contrib import admin
from .models import Job, JobService

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'job_type', 'status', 'priority', 'branch', 'assigned_to')
    list_filter = ('job_type', 'status', 'priority', 'branch')
    search_fields = ('title', 'description', 'customer__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(JobService)
class JobServiceAdmin(admin.ModelAdmin):
    list_display = ('job', 'service', 'quantity', 'price')
