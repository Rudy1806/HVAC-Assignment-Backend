from django.conf import settings
from django.db import models
from apps.tenants.models import Branch
from core.models import TenantAwareModel
from apps.customers.models import Customer
from apps.referrals.models import ReferralCode


LEAD_SOURCE_CHOICES = [
    ('tech_manual', 'Tech Manual'),
    ('qr_scan', 'QR Scan'),
    ('walk_in', 'Walk In'),
    ('other', 'Other'),
]

LEAD_STATUS_CHOICES = [
    ('new', 'New'),
    ('contacted', 'Contacted'),
    ('converted', 'Converted'),
    ('lost', 'Lost'),
]


class Lead(TenantAwareModel):
    """Sales leads with source tracking"""
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='leads'
    )
    name = models.CharField(max_length=255)
    mobile_num = models.CharField(max_length=20)
    email_id = models.EmailField(blank=True, null=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    referral_code = models.ForeignKey(
        ReferralCode, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='leads'
    )
    referred_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='leads_referred'
    )
    lead_source = models.CharField(max_length=20, choices=LEAD_SOURCE_CHOICES)
    status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, null=True)
    converted_customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='leads'
    )
    converted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='leads_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='leads_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"

    def __str__(self):
        return self.name
