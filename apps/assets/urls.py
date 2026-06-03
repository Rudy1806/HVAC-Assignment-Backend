from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    AssetTypeViewSet,
    AssetViewSet,
    AssetFieldViewSet,
    AssetFieldValueViewSet,
)

router = SimpleRouter()

router.register(
    r'asset-types',
    AssetTypeViewSet,
    basename='asset-types'
)

router.register(
    r'assets',
    AssetViewSet,
    basename='assets'
)

router.register(
    r'asset-fields',
    AssetFieldViewSet,
    basename='asset-fields'
)

router.register(
    r'asset-field-values',
    AssetFieldValueViewSet,
    basename='asset-field-values'
)

urlpatterns = [
    path('', include(router.urls)),
]