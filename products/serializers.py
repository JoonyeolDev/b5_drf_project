from rest_framework import serializers
from products.models import Product, ProductReview

class ProductReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductReview
        fields = ('score','content','price','store')

class ProductReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_username(self,obj):
        return obj.user.username
    
    def get_image(self,obj):
        if not obj.user.image:
            imagepath = 'images/default_profile.jpg'
        else: imagepath = obj.user.image
        return imagepath

    def get_likes_count(self,obj):
        return obj.likes.count()
    
    class Meta:
        model = ProductReview
        fields = ('id','username','image','score','content','price','store','likes','likes_count','updated_at')


class ProductListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self,obj):
        return obj.likes.count()

    class Meta:
        model = Product
        fields = ('id','name','image','brand','likes_count')


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name','introduction','image','brand')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'