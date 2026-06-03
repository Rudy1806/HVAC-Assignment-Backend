from rest_framework.routers import SimpleRouter

from .views import (
    CustomerViewSet,
    CustomerAddressViewSet,
)

router = SimpleRouter()

router.register(
    r'customers',
    CustomerViewSet,
    basename='customers'
)

router.register(
    r'customer-addresses',
    CustomerAddressViewSet,
    basename='customer-addresses'
)

urlpatterns = router.urls