from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .models import Job, JobService
from .serializers import (
    JobSerializer,
    JobServiceSerializer,
)


class JobViewSet(viewsets.ModelViewSet):

    serializer_class = JobSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter]

    search_fields = [
        'title',
        'description',
        'customer__name',
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Job.objects.select_related(
            'branch',
            'customer',
            'customer_address',
            'asset',
            'assigned_to',
        ).prefetch_related(
            'services'
        )

        return queryset.filter(
            branch=user.branch
        )


class JobServiceViewSet(viewsets.ModelViewSet):

    serializer_class = JobServiceSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        return JobService.objects.select_related(
            'job',
            'service'
        ).filter(
            job__branch=user.branch
        )