from rest_framework import serializers

from .models import Complaint

from apps.assets.models import Asset
from apps.customers.models import (
    Customer,
    CustomerAddress,
)


class ComplaintSerializer(serializers.ModelSerializer):

    class Meta:

        model = Complaint

        fields = [
            'id',

            'branch',

            'customer',
            'customer_address',
            'asset',

            'title',
            'description',

            'source',
            'priority',
            'status',

            'raised_by_customer',
            'raised_by_user',

            'converted_job',

            'converted_by',
            'converted_at',

            'updated_by',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'branch',

            'raised_by_customer',
            'raised_by_user',

            'converted_job',
            'converted_by',
            'converted_at',

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

        return attrs

    def create(self, validated_data):

        request = self.context.get('request')

        user = request.user

        validated_data['branch'] = user.branch

        validated_data['raised_by_user'] = user

        validated_data['updated_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):

        request = self.context.get('request')

        user = request.user

        validated_data['updated_by'] = user

        return super().update(instance, validated_data)