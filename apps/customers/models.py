from django.conf import settings
from django.db import models
from apps.tenants.models import Branch


CUSTOMER_TYPE_CHOICES = [
    ('residential', 'Residential'),
    ('commercial', 'Commercial'),
]


class Customer(models.Model):
    """
    Customer identity + billing entity.

    One customer can have multiple service addresses.
    """

    customer_id = models.BigAutoField(primary_key=True)

    

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='customers'
    )

    name = models.CharField(max_length=255)

    mobile_num = models.CharField(max_length=20)

    alternate_mobile_num = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    email_id = models.EmailField(blank=True, null=True)

    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPE_CHOICES,
        default='residential'
    )

    # Billing Address
    billing_address = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='customers_created'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers_updated'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['mobile_num']),
        ]

    def __str__(self):
        return self.name


class CustomerAddress(models.Model):
    """
    Multiple service locations for a customer.
    """

    address_id = models.BigAutoField(primary_key=True)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

   

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='customer_addresses'
    )

    service_address = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=20)

    landmark = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    lat = models.FloatField(null=True, blank=True)

    lon = models.FloatField(null=True, blank=True)

    is_default = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPE_CHOICES,
        default='residential'
    )

    class Meta:
        verbose_name = "Customer Address"
        verbose_name_plural = "Customer Addresses"

        ordering = ['-is_default', '-created_at']

        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['customer']),
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.city}"