"""
URL configuration for saas_hvac project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.auth import UserTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair_legacy'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh_legacy'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('apps.tenants.urls')),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.customers.urls')),
    path('', include('apps.customers.urls')),
    path('api/', include('apps.assets.urls')),
    path('api/', include('apps.complaints.urls')),
    path('api/', include('apps.amc.urls')),
    path('api/', include('apps.services.urls')),
    path('api/', include('apps.jobs.urls')),
    path('api/', include('apps.quotations.urls')),
    path('api/', include('apps.billing.urls')),
]
