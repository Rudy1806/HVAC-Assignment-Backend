from django.conf import settings
from django.db import models
from apps.tenants.models import Branch
from apps.customers.models import Customer
from apps.assets.models import Asset
from apps.jobs.models import Job
from apps.customers.models import CustomerAddress


COMPLAINT_SOURCE_CHOICES = [
    ('customer_app', 'Customer App'),
    ('technician_app', 'Technician App'),
    ('web', 'Web'),
]

COMPLAINT_PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('urgent', 'Urgent'),
]

COMPLAINT_STATUS_CHOICES = [

    ('open', 'Open'),

    ('acknowledged', 'Acknowledged'),

    ('assigned', 'Assigned'),

    ('scheduled', 'Scheduled'),

    ('technician_on_the_way', 'Technician On The Way'),

    ('in_progress', 'In Progress'),

    ('parts_pending', 'Parts Pending'),

    ('on_hold', 'On Hold'),

    ('completed', 'Completed'),

    ('closed', 'Closed'),

    ('cancelled', 'Cancelled'),

    ('rejected', 'Rejected'),
]


class Complaint(models.Model):
    """
    Customer complaints with multiple sources.
    
    Tenant isolation: complaints.branch.tenant
    Branch isolation: complaints.branch
    
    Note: Tenant is NOT stored directly; derived through branch.tenant
    """
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='complaints'
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='complaints'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='complaints'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    source = models.CharField(max_length=20, choices=COMPLAINT_SOURCE_CHOICES)
    priority = models.CharField(max_length=20, choices=COMPLAINT_PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=25, choices=COMPLAINT_STATUS_CHOICES, default='open')
    raised_by_customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='complaints_raised'
    )
    customer_address = models.ForeignKey(
    CustomerAddress,
    on_delete=models.CASCADE,
    related_name='complaints',
    null=True,
    blank=True
    )
    raised_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='complaints_raised'
    )
    converted_job = models.ForeignKey(
        Job, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='complaints'
    )
    converted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='complaints_converted'
    )
    converted_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='complaints_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"

    def __str__(self):
        return f"Complaint #{self.id} - {self.title}"
