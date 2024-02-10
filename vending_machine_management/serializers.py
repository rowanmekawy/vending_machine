from rest_framework import serializers
from vending_machine_management.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "amount_available",
            "cost",
            "product_name",
            "seller",
        )