from rest_framework import serializers

from .models import Job, JobService


class JobServiceSerializer(serializers.ModelSerializer):

    class Meta:

        model = JobService

        fields = [
            'id',

            'job',

            'service',

            'quantity',

            'price',
        ]


class JobSerializer(serializers.ModelSerializer):

    services = JobServiceSerializer(
        many=True,
        read_only=True
    )

    branch = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:

        model = Job

        fields = [
            'id',

            'branch',

            'customer',
            'customer_address',

            'asset',

            'job_type',

            'customer_amc',

            'title',
            'description',

            'status',
            'priority',

            'scheduled_at',
            'completed_at',

            'assigned_to',

            'created_by',
            'updated_by',

            'created_at',
            'updated_at',

            'services',
        ]

        read_only_fields = [
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

        if (
            customer and
            customer_address and
            customer_address.customer != customer
        ):

            raise serializers.ValidationError({
                'customer_address':
                    'Address does not belong to customer.'
            })

        if (
            asset and
            asset.customer != customer
        ):

            raise serializers.ValidationError({
                'asset':
                    'Asset does not belong to customer.'
            })

        return attrs

    def create(self, validated_data):

        request = self.context.get('request')

        user = request.user

        validated_data['branch'] = user.branch

        validated_data['created_by'] = user

        validated_data['updated_by'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):

        request = self.context.get('request')

        user = request.user

        validated_data['updated_by'] = user

        return super().update(instance, validated_data)