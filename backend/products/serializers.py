from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    # this is for making discount a valid attribute 
    discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            'title',
            'content',
            'price',
            'sale_price',
            'discount',
        ]
    
    def get_discount(self, obj):
        return obj.get_discount()
# if you have in models my_discount as a method , you do get_my_discount(self, obj)