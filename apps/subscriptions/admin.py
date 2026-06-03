from django.contrib import admin
from .models import SubscriptionPlan, TenantSubscription, Payment

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_monthly', 'price_yearly', 'max_users')

@admin.register(TenantSubscription)
class TenantSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'plan', 'status', 'start_date', 'end_date')
    list_filter = ('status',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('tenant__username', 'razorpay_payment_id')
