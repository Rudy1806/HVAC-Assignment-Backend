from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .models import (
    AMCPlan,
    AMCService,
    CustomerAMC,
)

from .serializers import (
    AMCPlanSerializer,
    AMCServiceSerializer,
    CustomerAMCSerializer,
)


class AMCPlanViewSet(viewsets.ModelViewSet):

    serializer_class = AMCPlanSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        return AMCPlan.objects.filter(
            tenant=user.tenant
        )


class AMCServiceViewSet(viewsets.ModelViewSet):

    serializer_class = AMCServiceSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        return AMCService.objects.select_related(
            'amc',
            'service',
        ).filter(
            amc__tenant=user.tenant
        )


class CustomerAMCViewSet(viewsets.ModelViewSet):

    serializer_class = CustomerAMCSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter]

    search_fields = [
        'customer__name',
        'asset__name',
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = CustomerAMC.objects.select_related(
            'tenant',
            'branch',

            'customer',
            'customer_address',

            'asset',

            'amc',

            'created_by',
            'updated_by',
        )

        # COMPANY_ADMIN
        if user.role == 'COMPANY_ADMIN':

            return queryset.filter(
                tenant=user.tenant
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