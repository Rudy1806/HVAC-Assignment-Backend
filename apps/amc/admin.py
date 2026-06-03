from django.contrib import admin
from .models import AMCPlan, AMCService, CustomerAMC

@admin.register(AMCPlan)
class AMCPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_months', 'tenant')
    list_filter = ('tenant',)
    search_fields = ('name',)

@admin.register(AMCService)
class AMCServiceAdmin(admin.ModelAdmin):
    list_display = ('amc', 'service', 'visits_per_year')

@admin.register(CustomerAMC)
class CustomerAMCAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amc', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'tenant')
    search_fields = ('customer__name', 'amc__name')
