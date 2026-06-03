from rest_framework import serializers

from .models import Customer, CustomerAddress


class CustomerAddressSerializer(serializers.ModelSerializer):

    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all()
    )

    class Meta:

        model = CustomerAddress

        fields = [
            'address_id',

            'customer',

            'service_address',
            'city',
            'state',
            'pincode',
            'landmark',
            'customer_type',

            'lat',
            'lon',

            'is_default',
            'is_active',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'address_id',
            'created_at',
            'updated_at',
        ]

class CustomerSerializer(serializers.ModelSerializer):

    addresses = CustomerAddressSerializer(
        many=True,
        read_only=True
    )
    branch = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Customer

        fields = [
            'customer_id',

            'branch',

            'name',
            'mobile_num',
            'alternate_mobile_num',
            'email_id',

            'customer_type',

            'billing_address',

            'is_active',

            'addresses',

            'created_by',
            'updated_by',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'customer_id',

            'created_by',
            'updated_by',

            'created_at',
            'updated_at',
        ]

    def validate_mobile_num(self, value):

        if len(value) < 10:
            raise serializers.ValidationError(
                "Mobile number must be at least 10 digits."
            )

        return value

    def validate(self, attrs):

        request = self.context.get('request')
        user = request.user

        branch = attrs.get('branch')

        # COMPANY_ADMIN can select branch
        if user.role == 'COMPANY_ADMIN':

            if not branch:
                raise serializers.ValidationError({
                    'branch': 'Branch is required.'
                })

            if branch.tenant != user.tenant:
                raise serializers.ValidationError({
                    'branch': 'Branch does not belong to your tenant.'
                })

        # Branch-level users auto-assign branch
        elif user.role in ['MANAGER', 'RECEPTIONIST', 'TECHNICIAN']:

            attrs['branch'] = user.branch

        return attrs

    def create(self, validated_data):

        request = self.context.get('request')
        user = request.user

        # Auto assign branch for branch-level users
        if user.role in ['MANAGER', 'RECEPTIONIST', 'TECHNICIAN']:
            validated_data['branch'] = user.branch

        validated_data['created_by'] = user
        validated_data['updated_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):

        request = self.context.get('request')
        user = request.user

        validated_data['updated_by'] = user

        return super().update(instance, validated_data)