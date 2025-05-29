from rest_framework import serializers

from .models import Category, Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'category',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'order',
            'quantity',
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'date_ordered',
            'items',
        ]
