from django.conf import settings
from django.db import models
from apps.tenants.models import Tenant, Branch
from core.models import TenantAwareModel


class ReferralCode(TenantAwareModel):
    """Technician referral codes with QR"""
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='referral_codes'
    )
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referral_codes'
    )
    code = models.CharField(max_length=50, unique=True)
    qr_url = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Referral Code"
        verbose_name_plural = "Referral Codes"

    def __str__(self):
        return f"{self.code} - {self.generated_by.username}"
