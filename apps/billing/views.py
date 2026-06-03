from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .models import (
    Invoice,
    InvoiceItem,
    Payment,
)

from .serializers import (
    InvoiceSerializer,
    InvoiceItemSerializer,
    PaymentSerializer,
)


class InvoiceViewSet(viewsets.ModelViewSet):

    serializer_class = InvoiceSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter]

    search_fields = [
        'invoice_no',
        'customer__name',
    ]

    def get_queryset(self):

        user = self.request.user

        return Invoice.objects.select_related(
            'customer',
            'customer_address',
            'job',
            'quotation',
        ).prefetch_related(
            'items',
            'payments',
        ).filter(
            tenant=user.tenant
        )


class InvoiceItemViewSet(viewsets.ModelViewSet):

    serializer_class = InvoiceItemSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        return InvoiceItem.objects.select_related(
            'invoice',
            'service',
        ).filter(
            invoice__tenant=user.tenant
        )


class PaymentViewSet(viewsets.ModelViewSet):

    serializer_class = PaymentSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        return Payment.objects.select_related(
            'invoice'
        ).filter(
            invoice__tenant=user.tenant
        )