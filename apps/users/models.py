from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.tenants.models import Branch, Tenant
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for multi-tenant SaaS.
    
    Platform Admin (superuser): tenant and branch are NULL
    Tenant Users: belong to a branch (and inherit tenant through branch.tenant)
    """
    class Role(models.TextChoices):
        COMPANY_ADMIN = 'COMPANY_ADMIN', 'Company Admin'
        MANAGER = 'MANAGER', 'Manager'
        RECEPTIONIST = 'RECEPTIONIST', 'Receptionist'
        TECHNICIAN = 'TECHNICIAN', 'Technician'

    user_id = models.BigAutoField(primary_key=True)
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='users',
        related_query_name='user',
        null=True,
        blank=True,
        help_text="NULL for superusers (Platform Admin). Auto-derived from branch for regular users."
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='branch_users',
        related_query_name='branch_user',
        null=True,
        blank=True,
        help_text="NULL for superusers (Platform Admin). Required for tenant users."
    )
    email_id = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    mobile_num = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email_id'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['tenant_id', 'branch_id', 'role', 'email_id']
        indexes = [
            models.Index(fields=['tenant', 'branch', 'role']),
            models.Index(fields=['email_id']),
        ]

    @property
    def id(self):
        return self.user_id

    @property
    def created_at(self):
        """Compatibility alias: some serializers expect created_at."""
        return self.date_joined

    def __str__(self):
        return self.email_id
