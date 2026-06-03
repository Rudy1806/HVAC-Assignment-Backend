from django.conf import settings
from django.db import models

from core.models import TenantAwareModel

from apps.customers.models import (
    Customer,
    CustomerAddress
)

from apps.jobs.models import Job
from apps.quotations.models import Quotation
from apps.services.models import Service


INVOICE_STATUS_CHOICES = [

    ('draft', 'Draft'),

    ('sent', 'Sent'),

    ('partially_paid', 'Partially Paid'),

    ('paid', 'Paid'),

    ('overdue', 'Overdue'),

    ('cancelled', 'Cancelled'),
]


class Invoice(TenantAwareModel):
    """
    Invoices generated from quotations.

    Complaint Flow:
        Complaint → Job → Quotation → Invoice → Payment

    AMC Flow:
        AMC → Quotation → Invoice → Payment → AMC Active
    """

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    customer_address = models.ForeignKey(
        CustomerAddress,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices'
    )

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices'
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices'
    )

    invoice_no = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    total_amount = models.FloatField()

    paid_amount = models.FloatField(
        default=0
    )

    balance_amount = models.FloatField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=INVOICE_STATUS_CHOICES,
        default='draft'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='invoices_created'
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices_updated'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

    def __str__(self):

        return f"Invoice #{self.id}"
        

class InvoiceItem(models.Model):
    """
    Snapshot of quotation items
    """

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoice_items'
    )

    description = models.CharField(
        max_length=255
    )

    quantity = models.IntegerField(
        default=1
    )

    price = models.FloatField()

    class Meta:
        verbose_name = "Invoice Item"
        verbose_name_plural = "Invoice Items"

    def __str__(self):

        return f"{self.invoice} - {self.description}"


PAYMENT_METHOD_CHOICES = [

    ('cash', 'Cash'),

    ('upi', 'UPI'),

    ('pay_later', 'Pay Later'),
]


PAYMENT_STATUS_CHOICES = [

    ('pending', 'Pending'),

    ('completed', 'Completed'),

    ('failed', 'Failed'),
]


class Payment(models.Model):

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.FloatField()

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    transaction_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):

        return f"Invoice #{self.invoice.id} - ₹{self.amount}"