from rest_framework import serializers

from .models import (
    AMCPlan,
    AMCService,
    CustomerAMC,
)

from apps.assets.models import Asset
from apps.customers.models import (
    Customer,
    CustomerAddress,
)


class AMCPlanSerializer(serializers.ModelSerializer):

    tenant = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:

        model = AMCPlan

        fields = [
            'id',

            'tenant',

            'name',
            'price',
            'duration_months',
        ]

        read_only_fields = [
            'tenant',
        ]

    def create(self, validated_data):

        request = self.context.get('request')

        user = request.user

        validated_data['tenant'] = user.tenant

        return super().create(validated_data)


class AMCServiceSerializer(serializers.ModelSerializer):

    class Meta:

        model = AMCService

        fields = [
            'id',

            'amc',

            'service',

            'visits_per_year',
        ]


class CustomerAMCSerializer(serializers.ModelSerializer):

    tenant = serializers.PrimaryKeyRelatedField(
    read_only=True
    )

    branch = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:

        model = CustomerAMC

        fields = [
            'id',

            'tenant',
            'branch',

            'customer',
            'customer_address',

            'asset',

            'amc',
            'manual_plan_name',
            'manual_price',
            'manual_duration_months',
            'start_date',
            'end_date',

            'visit_frequency',
            'custom_visits_per_year',

            'total_visits',
            'completed_visits',

            'status',

            'created_by',
            'updated_by',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'tenant',
            'branch',

            'created_by',
            'updated_by',

            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):

        customer = attrs.get('customer')

        customer_address = attrs.get('customer_address')

        asset = attrs.get('asset')
        

        # Address must belong to customer
        if (
            customer and
            customer_address and
            customer_address.customer != customer
        ):

            raise serializers.ValidationError({
                'customer_address':
                    'Address does not belong to customer.'
            })

        # Asset must belong to customer
        if (
            asset and
            asset.customer != customer
        ):

            raise serializers.ValidationError({
                'asset':
                    'Asset does not belong to customer.'
            })

        # Asset must belong to address
        if (
            asset and
            customer_address and
            asset.customer_address != customer_address
        ):

            raise serializers.ValidationError({
                'asset':
                    'Asset does not belong to customer address.'
            })
        
        amc = attrs.get('amc')

        manual_plan_name = attrs.get('manual_plan_name')

        # Require either predefined AMC or manual AMC
        if not amc and not manual_plan_name:

            raise serializers.ValidationError({
                'amc':
                    'Select AMC plan or create manual AMC.'
            })

        return attrs
    
    def create(self, validated_data):

        request = self.context.get('request')

        user = request.user

        validated_data['tenant'] = user.tenant

        validated_data['branch'] = user.branch

        validated_data['created_by'] = user

        validated_data['updated_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):

        request = self.context.get('request')

        user = request.user

        validated_data['updated_by'] = user

        return super().update(instance, validated_data)