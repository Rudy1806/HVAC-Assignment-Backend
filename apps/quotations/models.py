from django.conf import settings
from django.db import models
from core.models import TenantAwareModel
from apps.jobs.models import Job
from apps.services.models import Service


QUOTATION_STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('sent', 'Sent'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class Quotation(TenantAwareModel):
    """Quotations for complaint jobs"""
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='quotations'
    )
    total_amount = models.FloatField()
    status = models.CharField(
        max_length=20, choices=QUOTATION_STATUS_CHOICES, default='draft'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='quotations_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='quotations_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Quotation"
        verbose_name_plural = "Quotations"

    def __str__(self):
        return f"Quotation for Job #{self.job.id}"


class QuotationItem(models.Model):
    """Line items in a quotation"""
    quotation = models.ForeignKey(
        Quotation, on_delete=models.CASCADE, related_name='items'
    )
    service = models.ForeignKey(
    Service,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='quotation_items'
)

    description = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    
    quantity = models.IntegerField(default=1)
    price = models.FloatField()

    class Meta:
        verbose_name = "Quotation Item"
        verbose_name_plural = "Quotation Items"

    def __str__(self):
        return f"{self.quotation} - {self.service.name}"
