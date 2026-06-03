from django.db import models
from django.conf import settings
from apps.tenants.models import Tenant, Branch
from core.models import TenantAwareModel
from apps.customers.models import Customer
from apps.assets.models import Asset
from apps.services.models import Service
from apps.customers.models import CustomerAddress

class AMCPlan(TenantAwareModel):
    """Annual Maintenance Contract plans"""
    name = models.CharField(max_length=255)
    price = models.FloatField()
    duration_months = models.IntegerField(default=12)

    class Meta:
        verbose_name = "AMC Plan"
        verbose_name_plural = "AMC Plans"

    def __str__(self):
        return self.name


class AMCService(models.Model):
    """Services included in an AMC plan"""
    amc = models.ForeignKey(
        AMCPlan, on_delete=models.CASCADE, related_name='services'
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='amc_plans'
    )
    visits_per_year = models.IntegerField(
        default=2, help_text="Number of service visits per year"
    )

    class Meta:
        verbose_name = "AMC Service"
        verbose_name_plural = "AMC Services"
        unique_together = ('amc', 'service')

    def __str__(self):
        return f"{self.amc.name} - {self.service.name}"


AMC_STATUS_CHOICES = [

    ('draft', 'Draft'),

    ('active', 'Active'),

    ('expired', 'Expired'),

    ('cancelled', 'Cancelled'),

    ('completed', 'Completed'),

    ('pending_approval', 'Pending Approval'),
]

AMC_FREQUENCY_CHOICES = [

    ('monthly', 'Monthly'),

    ('quarterly', 'Quarterly'),

    ('half_yearly', 'Half Yearly'),

    ('yearly', 'Yearly'),

    ('custom', 'Custom'),
]

class CustomerAMC(TenantAwareModel):
    """AMC subscription for a customer's asset"""
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='customer_amcs'
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='amcs'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name='amcs'
    )
    amc = models.ForeignKey(
    AMCPlan,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='customer_subscriptions'
)
    customer_address = models.ForeignKey(
    CustomerAddress,
    on_delete=models.CASCADE,
    related_name='amcs',
    null=True,
    blank=True
)
    visit_frequency = models.CharField(
    max_length=20,
    choices=AMC_FREQUENCY_CHOICES,
    default='quarterly'
)
    custom_visits_per_year = models.IntegerField(
    null=True,
    blank=True
)
    total_visits = models.IntegerField(default=4)

    completed_visits = models.IntegerField(default=0)
    manual_plan_name = models.CharField(
    max_length=255,
    null=True,
    blank=True
)

    manual_price = models.FloatField(
    null=True,
    blank=True
)

    manual_duration_months = models.IntegerField(
    null=True,
    blank=True
)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=AMC_STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='amcs_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='amcs_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Customer AMC"
        verbose_name_plural = "Customer AMCs"

    def __str__(self):
        return f"{self.customer.name} - {self.amc.name}"
