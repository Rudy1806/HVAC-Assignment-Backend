from django.db import models
from apps.tenants.models import Tenant, Branch
from core.models import TenantAwareModel


ROLE_CHOICES = [
    ('owner', 'Owner'),
    ('manager', 'Manager'),
    ('technician', 'Technician'),
    ('support', 'Support'),
    ('customer', 'Customer'),
]


class User(TenantAwareModel):
    """Users with role-based access control"""
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name='users', null=True, blank=True
    )
    username = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    mobile_num = models.CharField(max_length=20)
    email_id = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        unique_together = ('tenant', 'email_id')

    def __str__(self):
        return f"{self.username} ({self.role})"
