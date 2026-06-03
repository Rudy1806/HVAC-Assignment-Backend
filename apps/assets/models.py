from django.conf import settings
from django.db import models
from apps.tenants.models import Tenant
from apps.customers.models import Customer
from apps.customers.models import CustomerAddress


class AssetType(models.Model):
    """
    Asset type classification (AC, Cooler, etc.).
    
    Note: AssetType is maintained at platform level.
    Tenant isolation through Assets that reference it.
    """
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Asset Type"
        verbose_name_plural = "Asset Types"

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    Physical assets belonging to customers.
    
    Tenant isolation: assets.customer.branch.tenant
    Branch isolation: assets.customer.branch
    
    Note: Tenant is NOT stored directly; derived through customer.branch.tenant
    """
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='assets'
    )
    asset_type = models.ForeignKey(
        AssetType, on_delete=models.SET_NULL, null=True, related_name='assets'
    )
    brand = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    serial_no = models.CharField(max_length=255, unique=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assets_created'
    )
    customer_address = models.ForeignKey(
    CustomerAddress,
    on_delete=models.CASCADE,
    related_name='assets',
    null=True,
    blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets_updated'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

    def __str__(self):
        return f"{self.name} ({self.serial_no})"


FIELD_TYPE_CHOICES = [
    ('text', 'Text'),
    ('number', 'Number'),
    ('date', 'Date'),
    ('boolean', 'Boolean'),
    ('select', 'Select'),
]


class AssetField(models.Model):
    """
    Dynamic fields for asset types.
    
    Note: AssetField is maintained at platform level like AssetType.
    Tenant isolation through Assets and their customers.
    """
    asset_type = models.ForeignKey(
        AssetType, on_delete=models.CASCADE, related_name='fields'
    )
    field_name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES)
    is_required = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Asset Field"
        verbose_name_plural = "Asset Fields"

    def __str__(self):
        return f"{self.asset_type.name} - {self.field_name}"


class AssetFieldValue(models.Model):
    """Values for dynamic asset fields"""
    asset = models.ForeignKey(
        Asset, on_delete=models.CASCADE, related_name='field_values'
    )
    field = models.ForeignKey(
        AssetField, on_delete=models.CASCADE, related_name='values'
    )
    value = models.TextField()

    class Meta:
        verbose_name = "Asset Field Value"
        verbose_name_plural = "Asset Field Values"
        unique_together = ('asset', 'field')

    def __str__(self):
        return f"{self.field.field_name}: {self.value}"
