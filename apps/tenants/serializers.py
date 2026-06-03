from rest_framework import serializers

from .models import Branch, Tenant


class TenantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    mobile_num = serializers.CharField(max_length=20)
    email_id = serializers.EmailField()
    address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    gst_num = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Tenant
        fields = ['tenant_id', 'name', 'email_id', 'mobile_num', 'address', 'gst_num', 'created_at', 'updated_at']

    def validate_mobile_num(self, value):
        if len(value) > 20:
            raise serializers.ValidationError('Mobile number must not exceed 20 characters.')
        return value

    def create(self, validated_data):
        tenant = Tenant(**validated_data)
        tenant.save()
        return tenant

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BranchSerializer(serializers.ModelSerializer):
    # Require tenant PK on create/update so validation fails cleanly if missing
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())
    name = serializers.CharField(max_length=255)
    address = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    mobile_num = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)
    email_id = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    gst_num = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Branch
        fields = ['branch_id', 'tenant', 'name', 'address', 'mobile_num', 'email_id', 'gst_num']

    def validate_mobile_num(self, value):
        if value and len(value) > 20:
            raise serializers.ValidationError('Branch mobile number must not exceed 20 characters.')
        return value
