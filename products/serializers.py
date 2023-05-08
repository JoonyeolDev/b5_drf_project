from rest_framework import serializers
from products.models import Product

class ProductListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ('name','image','brand')


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'
