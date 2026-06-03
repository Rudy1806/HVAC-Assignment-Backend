from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .models import (
    Quotation,
    QuotationItem,
)

from .serializers import (
    QuotationSerializer,
    QuotationItemSerializer,
)


class QuotationViewSet(viewsets.ModelViewSet):

    serializer_class = QuotationSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter]

    search_fields = [
        'job__title',
    ]

    def get_queryset(self):

        user = self.request.user

        return Quotation.objects.select_related(
            'job',
            'created_by',
            'updated_by',
        ).prefetch_related(
            'items'
        ).filter(
            tenant=user.tenant
        )


class QuotationItemViewSet(viewsets.ModelViewSet):

    serializer_class = QuotationItemSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        return QuotationItem.objects.select_related(
            'quotation',
            'service',
        ).filter(
            quotation__tenant=user.tenant
        )