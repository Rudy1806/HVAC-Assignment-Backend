from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BranchViewSet, TenantViewSet

router = DefaultRouter()
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'branches', BranchViewSet, basename='branch')

urlpatterns = [
    path('', include(router.urls)),
]
