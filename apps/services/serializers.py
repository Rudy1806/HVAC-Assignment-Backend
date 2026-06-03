from rest_framework import serializers

from .models import Service


class ServiceSerializer(serializers.ModelSerializer):

    tenant = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:

        model = Service

        fields = [
            'id',

            'tenant',

            'name',
            'description',

            'category',

            'cost',
            'price',

            'gst_percent',

            'is_active',
        ]

        read_only_fields = [
            'tenant',
        ]

    def create(self, validated_data):

        request = self.context.get('request')

        validated_data['tenant'] = request.user.tenant

        return super().create(validated_data)