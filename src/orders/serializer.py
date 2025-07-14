from django.db import transaction
from rest_framework import serializers

from products.models import Product
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')
    products = serializers.SlugRelatedField(
        queryset = Product.objects.all(),
        many=True,
        read_only=False,
        slug_field='id'
    )

    class Meta:
        model = Order
        fields = ['id', 'products', 'created_at', 'created_by']
        read_only_fields = ['id', 'created_at', 'created_by']

    @transaction.atomic
    def create(self, validated_data:dict):
        request = self.context.get('request')
        user = request.user

        order = Order.objects.create(created_by=user)

        products = validated_data.pop('products')
        order.products.set(products)

        return order
    
    @transaction.atomic
    def update(self, instance:Order, validated_data:dict):
        request = self.context.get('request')

        products = validated_data.get('products', instance.products)
        if request.method == 'PATCH':
            instance.products.add(*products)
        else:
            instance.products.set(products)

        return instance