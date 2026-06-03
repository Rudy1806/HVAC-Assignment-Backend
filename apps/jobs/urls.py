from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    JobViewSet,
    JobServiceViewSet,
)

router = DefaultRouter()

router.register(
    r'jobs',
    JobViewSet,
    basename='jobs'
)

router.register(
    r'job-services',
    JobServiceViewSet,
    basename='job-services'
)

urlpatterns = [
    path('', include(router.urls)),
]