from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    AMCPlanViewSet,
    AMCServiceViewSet,
    CustomerAMCViewSet,
)

router = SimpleRouter()

router.register(
    r'amc-plans',
    AMCPlanViewSet,
    basename='amc-plans'
)

router.register(
    r'amc-services',
    AMCServiceViewSet,
    basename='amc-services'
)

router.register(
    r'customer-amcs',
    CustomerAMCViewSet,
    basename='customer-amcs'
)

urlpatterns = [
    path('', include(router.urls)),
]