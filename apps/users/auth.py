from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = 'SUPERUSER' if user.is_superuser else user.role
        token['is_superuser'] = user.is_superuser
        token['branch_id'] = user.branch_id
        token['tenant_id'] = user.tenant.tenant_id if user.tenant else None
        return token


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
