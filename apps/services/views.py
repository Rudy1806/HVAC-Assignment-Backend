from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(viewsets.ModelViewSet):

    serializer_class = ServiceSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter]

    search_fields = [
        'name',
        'description',
        'category',
    ]

    def get_queryset(self):

        user = self.request.user

        return Service.objects.filter(
            tenant=user.tenant
        ).order_by('name')