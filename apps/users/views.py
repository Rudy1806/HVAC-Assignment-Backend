from rest_framework import exceptions, permissions, viewsets

from .models import User
from .serializers import UserCreateSerializer, UserListSerializer, UserUpdateSerializer


class UserViewSet(viewsets.ModelViewSet):
    """CRUD API for tenant-isolated branch users."""

    queryset = User.objects.select_related('branch__tenant').all().order_by('branch__tenant_id', 'branch_id', 'role', 'email_id')
    permission_classes = [permissions.IsAuthenticated]

    def get_current_tenant(self):
        user = getattr(self.request, 'user', None)
        if not user or not user.is_authenticated:
            return None
        if user.is_superuser:
            return None
        if user.tenant is not None:
            return user.tenant
        if getattr(user, 'branch', None) is not None:
            return user.branch.tenant
        return None

    def get_queryset(self):
        user = getattr(self.request, 'user', None)
        if not user or not user.is_authenticated:
            return User.objects.none()

        tenant = self.get_current_tenant()
        queryset = self.queryset
        if tenant is not None:
            queryset = queryset.filter(branch__tenant=tenant)

        role = self.request.query_params.get('role')
        branch_id = self.request.query_params.get('branch_id')
        if role:
            queryset = queryset.filter(role=role)
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserListSerializer

    def perform_create(self, serializer):
        branch = serializer.validated_data.get('branch')
        user = self.request.user
        if not user.is_superuser:
            tenant = self.get_current_tenant()
            if branch.tenant != tenant:
                raise exceptions.ValidationError('Branch must belong to the logged-in tenant.')
        serializer.save()

    def perform_update(self, serializer):
        branch = serializer.validated_data.get('branch', serializer.instance.branch)
        user = self.request.user
        if not user.is_superuser:
            tenant = self.get_current_tenant()
            if branch.tenant != tenant:
                raise exceptions.ValidationError('Branch must belong to the logged-in tenant.')
        serializer.save()
