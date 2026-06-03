from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ComplaintViewSet

router = SimpleRouter()

router.register(
    r'complaints',
    ComplaintViewSet,
    basename='complaints'
)

urlpatterns = [
    path('', include(router.urls)),
]