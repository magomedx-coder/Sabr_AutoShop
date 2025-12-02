from rest_framework import serializers
from shop.models import *


class GoodItemSerializer(serializers.ModelSerializer):
    item = serializers.ReadOnlyField(source='item.name')

    class Meta:
        model = GoodItem
        fields = ['item', 'quantity', 'price']


class InvoiceSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    gooditem_set = GoodItemSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'get_total_cost', 'author', 'created_at', 'gooditem_set']
