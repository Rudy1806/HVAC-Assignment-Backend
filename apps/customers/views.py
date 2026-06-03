from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .models import Customer, CustomerAddress
from .serializers import (
    CustomerSerializer,
    CustomerAddressSerializer,
)


class CustomerViewSet(viewsets.ModelViewSet):

    serializer_class = CustomerSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter]

    search_fields = [
        'name',
        'mobile_num',
        'email_id',
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Customer.objects.select_related(
            'branch',
            'branch__tenant',
            'created_by',
            'updated_by',
        ).prefetch_related(
            'addresses'
        )

        # COMPANY_ADMIN
        if user.role == 'COMPANY_ADMIN':

            return queryset.filter(
                branch__tenant=user.tenant
            )

        # Branch-level users
        elif user.role in [
            'MANAGER',
            'RECEPTIONIST',
            'TECHNICIAN'
        ]:

            return queryset.filter(
                branch=user.branch
            )

        return queryset.none()


class CustomerAddressViewSet(viewsets.ModelViewSet):

    serializer_class = CustomerAddressSerializer

    permission_classes = [IsAuthenticated]

    

    def get_queryset(self):

        user = self.request.user

        queryset = CustomerAddress.objects.select_related(
            'customer',
            'branch',
            'branch__tenant',
        )

        # COMPANY_ADMIN
        if user.role == 'COMPANY_ADMIN':

            return queryset.filter(
                branch__tenant=user.tenant
            )

        # Branch-level users
        elif user.role in [
            'MANAGER',
            'RECEPTIONIST',
            'TECHNICIAN'
        ]:

            return queryset.filter(
                branch=user.branch
            )

        return queryset.none()
    
    def perform_create(self, serializer):

        user = self.request.user

        customer = serializer.validated_data.get('customer')

        # COMPANY_ADMIN
        if user.role == 'COMPANY_ADMIN':

            serializer.save(
                customer=customer,
                branch=customer.branch
            )

        # Branch-level users
        elif user.role in [
            'MANAGER',
            'RECEPTIONIST',
            'TECHNICIAN'
        ]:

            serializer.save(
                customer=customer,
                branch=user.branch
            )

