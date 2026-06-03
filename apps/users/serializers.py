from rest_framework import serializers

from apps.tenants.models import Branch, Tenant
from .models import User


class UserListSerializer(serializers.ModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(read_only=True)
    tenant_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id', 'full_name', 'email_id', 'mobile_num',
            'role', 'branch', 'tenant_id', 'is_active', 'is_staff',
            'date_joined', 'updated_at'
        ]

    def get_tenant_id(self, obj):
        if obj.tenant is not None:
            return obj.tenant.tenant_id
        if obj.branch is not None:
            return obj.branch.tenant_id
        return None


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    tenant = serializers.PrimaryKeyRelatedField(
    queryset=Tenant.objects.all(),
    required=False,
    allow_null=True
)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'full_name', 'email_id', 'mobile_num',
            'password', 'role', 'tenant', 'branch', 'is_active', 'is_staff',
            'date_joined', 'updated_at'
        ]
        read_only_fields = ['user_id', 'date_joined', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and getattr(request.user, 'is_authenticated', False):
            # All users can see all tenants if superuser; otherwise only their own tenant
            if request.user.is_superuser:
                self.fields['tenant'].queryset = Tenant.objects.all()
                self.fields['branch'].queryset = Branch.objects.all()
            else:
                user_tenant = getattr(request.user, 'tenant', None)
                if user_tenant:
                    self.fields['tenant'].queryset = Tenant.objects.filter(pk=user_tenant.pk)
                    self.fields['branch'].queryset = Branch.objects.filter(tenant=user_tenant)
        else:
            self.fields['tenant'].queryset = Tenant.objects.all()

    def validate_email_id(self, value):
        if User.objects.filter(email_id__iexact=value).exists():
            raise serializers.ValidationError('A user with this email_id already exists.')
        return value

    def validate(self, data):
        role = data.get('role')
        tenant = data.get('tenant')
        branch = data.get('branch')

        # Superuser: no validation needed
        request = self.context.get('request')
        if request and request.user.is_superuser:
            return data

        # Company admin: tenant required, branch optional
        if role == User.Role.COMPANY_ADMIN:
            if not tenant:
                raise serializers.ValidationError(
                    {'tenant': 'A tenant is required for Company Admin users.'},
                    code='required'
                )
            if branch and branch.tenant != tenant:
                raise serializers.ValidationError(
                    {'branch': 'Branch must belong to the selected tenant.'},
                    code='invalid'
                )
            return data

        # Manager, Technician, Receptionist: both required
        if role in (User.Role.MANAGER, User.Role.TECHNICIAN, User.Role.RECEPTIONIST):
            if not tenant:
                raise serializers.ValidationError(
                    {'tenant': 'A tenant is required for this role.'},
                    code='required'
                )
            if not branch:
                raise serializers.ValidationError(
                    {'branch': 'A branch is required for this role.'},
                    code='required'
                )
            if branch.tenant != tenant:
                raise serializers.ValidationError(
                    {'branch': 'Branch must belong to the selected tenant.'},
                    code='invalid'
                )
            return data

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        branch = validated_data.get('branch')
        tenant = validated_data.get('tenant')

        # If branch is provided but tenant is not, derive tenant from branch
        if branch and not tenant:
            validated_data['tenant'] = branch.tenant

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=8)
    tenant = serializers.PrimaryKeyRelatedField(
    queryset=Tenant.objects.all(),
    required=False,
    allow_null=True
)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'full_name', 'email_id', 'mobile_num',
            'password', 'role', 'tenant', 'branch', 'is_active', 'is_staff',
            'date_joined', 'updated_at'
        ]
        read_only_fields = ['user_id', 'date_joined', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and getattr(request.user, 'is_authenticated', False):
            if request.user.is_superuser:
                self.fields['tenant'].queryset = Tenant.objects.all()
                self.fields['branch'].queryset = Branch.objects.all()
            else:
                user_tenant = getattr(request.user, 'tenant', None)
                if user_tenant:
                    self.fields['tenant'].queryset = Tenant.objects.filter(pk=user_tenant.pk)
                    self.fields['branch'].queryset = Branch.objects.filter(tenant=user_tenant)
        else:
            self.fields['tenant'].queryset = Tenant.objects.all()

    def validate_email_id(self, value):
        user = self.instance
        if User.objects.filter(email_id__iexact=value).exclude(user_id=user.user_id).exists():
            raise serializers.ValidationError('A user with this email_id already exists.')
        return value

    def validate(self, data):
        role = data.get('role', self.instance.role)
        tenant = data.get('tenant', self.instance.tenant)
        branch = data.get('branch', self.instance.branch)

        

        # Company admin: tenant required, branch optional
        if role == User.Role.COMPANY_ADMIN:
            if not tenant:
                raise serializers.ValidationError(
                    {'tenant': 'A tenant is required for Company Admin users.'},
                    code='required'
                )
            if branch and branch.tenant != tenant:
                raise serializers.ValidationError(
                    {'branch': 'Branch must belong to the selected tenant.'},
                    code='invalid'
                )
            return data

        # Manager, Technician, Receptionist: both required
        if role in (User.Role.MANAGER, User.Role.TECHNICIAN, User.Role.RECEPTIONIST):
            if not tenant:
                raise serializers.ValidationError(
                    {'tenant': 'A tenant is required for this role.'},
                    code='required'
                )
            if not branch:
                raise serializers.ValidationError(
                    {'branch': 'A branch is required for this role.'},
                    code='required'
                )
            if branch.tenant != tenant:
                raise serializers.ValidationError(
                    {'branch': 'Branch must belong to the selected tenant.'},
                    code='invalid'
                )
            return data

        return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        branch = validated_data.get('branch', instance.branch)
        tenant = validated_data.get('tenant', instance.tenant)

        # If branch is provided but tenant is not, derive tenant from branch
        if branch and not tenant:
            validated_data['tenant'] = branch.tenant

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
