from rest_framework import serializers

from .models import (
    Invoice,
    InvoiceItem,
    Payment,
)


class InvoiceItemSerializer(serializers.ModelSerializer):

    class Meta:

        model = InvoiceItem

        fields = [
            'id',

            'invoice',

            'service',

            'description',

            'quantity',

            'price',
        ]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Payment

        fields = [
            'id',

            'invoice',

            'amount',

            'payment_method',

            'payment_status',

            'transaction_id',

            'payment_date',
        ]

        read_only_fields = [
            'payment_date',
        ]


class InvoiceSerializer(serializers.ModelSerializer):

    items = InvoiceItemSerializer(
        many=True,
        read_only=True
    )

    payments = PaymentSerializer(
        many=True,
        read_only=True
    )

    tenant = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:

        model = Invoice

        fields = [
            'id',

            'tenant',

            'customer',
            'customer_address',

            'quotation',
            'job',

            'invoice_no',

            'total_amount',
            'paid_amount',
            'balance_amount',

            'status',

            'created_by',
            'updated_by',

            'created_at',
            'updated_at',

            'items',
            'payments',
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

        if not validated_data.get('balance_amount'):

            validated_data['balance_amount'] = (
                validated_data['total_amount']
            )

        return super().create(validated_data)

    def update(self, instance, validated_data):

        validated_data['updated_by'] = (
            self.context['request'].user
        )

        return super().update(
            instance,
            validated_data
        )