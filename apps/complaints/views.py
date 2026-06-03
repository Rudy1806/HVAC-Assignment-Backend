from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .models import Complaint
from .serializers import ComplaintSerializer


class ComplaintViewSet(viewsets.ModelViewSet):

    serializer_class = ComplaintSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter]

    search_fields = [
        'title',
        'description',
        'customer__name',
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Complaint.objects.select_related(
            'branch',

            'customer',
            'customer_address',

            'asset',

            'raised_by_user',
            'updated_by',
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