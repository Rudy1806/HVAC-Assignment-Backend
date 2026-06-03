from django.conf import settings
from django.db import models
from apps.tenants.models import Branch
from apps.customers.models import Customer
from apps.assets.models import Asset
from apps.amc.models import CustomerAMC
from apps.services.models import Service
from apps.customers.models import CustomerAddress


JOB_TYPE_CHOICES = [
    ('amc', 'AMC'),
    ('complaint', 'Complaint'),
]

JOB_STATUS_CHOICES = [

    ('created', 'Created'),

    ('assigned', 'Assigned'),

    ('scheduled', 'Scheduled'),

    ('started', 'Started'),

    ('diagnosis_completed', 'Diagnosis Completed'),

    ('quotation_pending', 'Quotation Pending'),

    ('quotation_approved', 'Quotation Approved'),

    ('work_in_progress', 'Work In Progress'),

    ('completed', 'Completed'),

    ('closed', 'Closed'),

    ('cancelled', 'Cancelled'),
]

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('urgent', 'Urgent'),
]


class Job(models.Model):
    """
    Service jobs.
    
    Tenant isolation: jobs.branch.tenant
    Branch isolation: jobs.branch
    
    Note: Tenant is NOT stored directly; derived through branch.tenant
    """
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='jobs'
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='jobs'
    )
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name='jobs', null=True, blank=True
    )
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    customer_amc = models.ForeignKey(
        CustomerAMC, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='jobs'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_jobs'
    )
    customer_address = models.ForeignKey(
    CustomerAddress,
    on_delete=models.CASCADE,
    related_name='jobs',
    null=True,
    blank=True
)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='jobs_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return f"Job #{self.id} - {self.title}"


class JobService(models.Model):
    """Services rendered in a job"""
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='services'
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='job_services'
    )
    quantity = models.IntegerField(default=1)
    price = models.FloatField(help_text="Final charged price; 0 for AMC-covered")

    class Meta:
        verbose_name = "Job Service"
        verbose_name_plural = "Job Services"
        unique_together = ('job', 'service')

    def __str__(self):
        return f"{self.job.title} - {self.service.name}"
