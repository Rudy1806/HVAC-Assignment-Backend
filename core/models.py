from django.db import models

from apps.tenants.models import Tenant


class TenantAwareModel(models.Model):
    """Abstract base model to provide tenant FK for tenant-isolated models."""
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, db_index=True
    )

    class Meta:
        abstract = True
