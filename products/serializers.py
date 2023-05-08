from rest_framework import serializers
from products.models import Product

class ProductListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self,obj):
        return obj.likes.count()

    class Meta:
        model = Product
        fields = ('name','image','brand','likes_count')


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'
