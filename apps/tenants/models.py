from django.db import models


class Tenant(models.Model):
    tenant_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email_id = models.EmailField(unique=True)
    mobile_num = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gst_num = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tenants_tenant'
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'

    def __str__(self):
        return self.name


class Branch(models.Model):
    branch_id = models.BigAutoField(primary_key=True)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='branches',
        related_query_name='branch'
    )
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    mobile_num = models.CharField(max_length=20, blank=True, null=True)
    email_id = models.EmailField(blank=True, null=True)
    gst_num = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tenants_branch'
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        unique_together = [['tenant', 'name']]

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"
