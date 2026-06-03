from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .models import (
    AssetType,
    Asset,
    AssetField,
    AssetFieldValue,
)

from .serializers import (
    AssetTypeSerializer,
    AssetSerializer,
    AssetFieldSerializer,
    AssetFieldValueSerializer,
)


class AssetTypeViewSet(viewsets.ModelViewSet):

    queryset = AssetType.objects.all()

    serializer_class = AssetTypeSerializer

    permission_classes = [IsAuthenticated]


class AssetViewSet(viewsets.ModelViewSet):

    serializer_class = AssetSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter]

    search_fields = [
        'name',
        'serial_no',
        'brand',
        'model',
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Asset.objects.select_related(
            'customer',
            'customer_address',
            'asset_type',
            'created_by',
            'updated_by',
        ).prefetch_related(
            'field_values'
        )

        # COMPANY_ADMIN
        if user.role == 'COMPANY_ADMIN':

            return queryset.filter(
                customer__branch__tenant=user.tenant
            )

        # Branch-level users
        elif user.role in [
            'MANAGER',
            'RECEPTIONIST',
            'TECHNICIAN'
        ]:

            return queryset.filter(
                customer__branch=user.branch
            )

        return queryset.none()


class AssetFieldViewSet(viewsets.ModelViewSet):

    queryset = AssetField.objects.all()

    serializer_class = AssetFieldSerializer

    permission_classes = [IsAuthenticated]


class AssetFieldValueViewSet(viewsets.ModelViewSet):

    queryset = AssetFieldValue.objects.all()

    serializer_class = AssetFieldValueSerializer

    permission_classes = [IsAuthenticated]