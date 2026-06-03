from rest_framework import exceptions, permissions, serializers, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from .auth import TenantTokenObtainPairSerializer
from .models import Branch, Tenant
from .serializers import BranchSerializer, TenantSerializer


class TenantViewSet(viewsets.ModelViewSet):
    """CRUD API for Tenant records."""

    queryset = Tenant.objects.all().order_by('-created_at')
    serializer_class = TenantSerializer


class TenantTokenView(TokenObtainPairView):
    serializer_class = TenantTokenObtainPairSerializer


class BranchViewSet(viewsets.ModelViewSet):
    """CRUD API for Branch records with tenant isolation."""

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_current_tenant(self):
        if not getattr(self.request, 'user', None) or not self.request.user.is_authenticated:
            return None

        if self.request.user.is_superuser:
            return None

        user_tenant = getattr(self.request.user, 'tenant', None)
        if user_tenant is not None:
            return user_tenant

        if getattr(self.request.user, 'branch', None) is not None:
            return self.request.user.branch.tenant

        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        user = getattr(self.request, 'user', None)
        if not user or not user.is_authenticated:
            return Branch.objects.none()

        if user.is_superuser:
            return queryset

        tenant = self.get_current_tenant()
        if tenant is None:
            raise exceptions.PermissionDenied('Authenticated user is not assigned to a tenant.')
        return queryset.filter(tenant=tenant)

    def perform_create(self, serializer):
        # Allow serializer to validate and set `tenant` from the request data.
        # This ensures missing tenant triggers serializer validation errors
        # (e.g. {"tenant": ["This field is required."]}) instead of DB IntegrityError.
        serializer.save()
