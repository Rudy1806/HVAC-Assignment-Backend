from django.db import models
from core.models import TenantAwareModel

SERVICE_CATEGORY_CHOICES = [

    ('complaint', 'Complaint'),

    ('amc', 'AMC'),

    ('installation', 'Installation'),

    ('repair', 'Repair'),

    ('inspection', 'Inspection'),

    ('general', 'General'),
]

class Service(TenantAwareModel):
    """Services offered by the tenant"""

    name = models.CharField(max_length=255)

    description = models.TextField(
        blank=True,
        null=True
    )

    cost = models.FloatField(
        help_text="Internal cost"
    )

    price = models.FloatField(
        help_text="Selling price"
    )

    gst_percent = models.FloatField(
        default=18.0
    )

    category = models.CharField(
        max_length=30,
        choices=SERVICE_CATEGORY_CHOICES,
        default='general'
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['name']

    def __str__(self):
        return self.name