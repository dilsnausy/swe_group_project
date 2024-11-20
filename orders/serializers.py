from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'product', 'quantity', 'total_price', 'order_date', 'status']
