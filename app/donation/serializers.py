# app/donation/serializers.py

from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'stream', 'user', 'amount', 'payment_method', 'payment_status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'payment_status', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set the default values for user and payment_status
        validated_data['user'] = self.context['request'].user
        validated_data['payment_status'] = 'pending'
        return super().create(validated_data)
