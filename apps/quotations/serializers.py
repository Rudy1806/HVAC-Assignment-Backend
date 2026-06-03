from rest_framework import serializers

from .models import (
    Quotation,
    QuotationItem,
)


class QuotationItemSerializer(serializers.ModelSerializer):

    class Meta:

        model = QuotationItem

        fields = [
            'id',

            'quotation',

            'service',

            'description',

            'quantity',

            'price',
        ]


class QuotationSerializer(serializers.ModelSerializer):

    items = QuotationItemSerializer(
        many=True,
        read_only=True
    )

    tenant = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:

        model = Quotation

        fields = [
            'id',

            'tenant',

            'job',

            'total_amount',

            'status',

            'created_by',
            'updated_by',

            'created_at',
            'updated_at',

            'items',
        ]

        read_only_fields = [
            'tenant',

            'created_by',
            'updated_by',

            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):

        user = self.context['request'].user

        validated_data['tenant'] = user.tenant

        validated_data['created_by'] = user

        validated_data['updated_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):

        validated_data['updated_by'] = (
            self.context['request'].user
        )

        return super().update(
            instance,
            validated_data
        )