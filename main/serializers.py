from rest_framework import serializers

from .models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        read_only_fields = ('order_id', 'timestamp', 'price', 'account')
        fields = '__all__'
