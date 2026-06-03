from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Tenant


class TenantTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email_id'

    @classmethod
    def get_token(cls, tenant):
        token = super().get_token(tenant)
        token['tenant_id'] = str(tenant.id)
        token['email_id'] = tenant.email_id
        return token

    def validate(self, attrs):
        email = attrs.get('email_id')
        password = attrs.get('password')

        if not email or not password:
            raise AuthenticationFailed('Email and password are required.')

        try:
            tenant = Tenant.objects.get(email_id=email)
        except Tenant.DoesNotExist:
            raise AuthenticationFailed('No tenant found with this email.')

        if not tenant.check_password(password):
            raise AuthenticationFailed('Incorrect email or password.')

        refresh = self.get_token(tenant)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return data


class TenantJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        tenant_id = validated_token.get('user_id') or validated_token.get('tenant_id')
        if tenant_id is None:
            raise InvalidToken('Token contained no recognizable tenant id')

        try:
            return Tenant.objects.get(pk=tenant_id)
        except Tenant.DoesNotExist:
            raise AuthenticationFailed('Tenant not found.', code='user_not_found')
