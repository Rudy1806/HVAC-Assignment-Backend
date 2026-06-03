from django.db import models
from apps.tenants.models import Tenant


class SubscriptionPlan(models.Model):
    """Tenant subscription plans"""
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=255, choices=PLAN_CHOICES)
    price_monthly = models.FloatField()
    price_yearly = models.FloatField()
    max_users = models.IntegerField()
    max_branches = models.IntegerField()
    max_assets = models.IntegerField()
    has_amc = models.BooleanField(default=False)
    has_reports = models.BooleanField(default=False)
    has_whatsapp = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Subscription Plan"
        verbose_name_plural = "Subscription Plans"

    def __str__(self):
        return self.name


SUBSCRIPTION_STATUS_CHOICES = [
    ('trial', 'Trial'),
    ('active', 'Active'),
    ('expired', 'Expired'),
    ('cancelled', 'Cancelled'),
]

BILLING_CYCLE_CHOICES = [
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
]


class TenantSubscription(models.Model):
    """Tenant's active subscription"""
    tenant = models.OneToOneField(
        Tenant, on_delete=models.CASCADE, related_name='subscription'
    )
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.SET_NULL, null=True, related_name='subscriptions'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=SUBSCRIPTION_STATUS_CHOICES, default='active'
    )
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES)
    amount_paid = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tenant Subscription"
        verbose_name_plural = "Tenant Subscriptions"

    def __str__(self):
        return f"{self.tenant.username} - {self.plan.name}"


PAYMENT_STATUS_CHOICES = [
    ('created', 'Created'),
    ('pending', 'Pending'),
    ('success', 'Success'),
    ('failed', 'Failed'),
]

PAYMENT_METHOD_CHOICES = [
    ('card', 'Card'),
    ('upi', 'UPI'),
    ('netbanking', 'NetBanking'),
]


class Payment(models.Model):
    """Payment records for subscriptions"""
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name='payments'
    )
    subscription = models.ForeignKey(
        TenantSubscription, on_delete=models.CASCADE, related_name='payments'
    )
    amount = models.FloatField()
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='created')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    transaction_ref = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment {self.id} - {self.tenant.username}"
