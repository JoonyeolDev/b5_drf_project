from rest_framework import serializers
from products.models import Product, ProductReview

class ProductReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductReview
        fields = ('score','content','price','store')

class ProductReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self,obj):
        return obj.likes.count()
    
    class Meta:
        model = ProductReview
        fields = ('score','content','price','store','likes_count')


class ProductListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self,obj):
        return obj.likes.count()

    class Meta:
        model = Product
        fields = ('name','image','brand','likes_count')


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','introdution','image','brand')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'