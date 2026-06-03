from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    QuotationViewSet,
    QuotationItemViewSet,
)

router = DefaultRouter()

router.register(
    r'quotations',
    QuotationViewSet,
    basename='quotations'
)

router.register(
    r'quotation-items',
    QuotationItemViewSet,
    basename='quotation-items'
)

urlpatterns = [
    path('', include(router.urls)),
]