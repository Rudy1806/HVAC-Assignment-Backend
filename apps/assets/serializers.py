from rest_framework import serializers

from .models import (
    AssetType,
    Asset,
    AssetField,
    AssetFieldValue,
)


class AssetTypeSerializer(serializers.ModelSerializer):

    class Meta:

        model = AssetType

        fields = '__all__'


class AssetFieldSerializer(serializers.ModelSerializer):

    class Meta:

        model = AssetField

        fields = '__all__'


class AssetFieldValueSerializer(serializers.ModelSerializer):

    class Meta:

        model = AssetFieldValue

        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):

    field_values = AssetFieldValueSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Asset

        fields = [
            'id',

            'customer',
            'customer_address',

            'asset_type',

            'brand',
            'name',
            'model',
            'serial_no',
            'area',

            'created_by',
            'updated_by',

            'created_at',
            'updated_at',

            'field_values',
        ]

        read_only_fields = [
            'created_by',
            'updated_by',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):

        customer = attrs.get('customer')
        customer_address = attrs.get('customer_address')

        # Ensure address belongs to customer
        if (
            customer and
            customer_address and
            customer_address.customer != customer
        ):

            raise serializers.ValidationError({
                'customer_address':
                    'Address does not belong to customer.'
            })

        return attrs

    def create(self, validated_data):

        request = self.context.get('request')

        user = request.user

        validated_data['created_by'] = user
        validated_data['updated_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):

        request = self.context.get('request')

        user = request.user

        validated_data['updated_by'] = user

        return super().update(instance, validated_data)