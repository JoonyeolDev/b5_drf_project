from rest_framework import serializers
from users.models import User
from posts.serializers import PostingSerializer
from products.serializers import ProductReviewSerializer, ProductListSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "username", "gender", "date_of_birth", "preference", "introduction", "image")
        read_only_fields = ["email",]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        instance.preference = validated_data.get("preference", instance.preference)
        instance.introduction = validated_data.get(
            "introduction", instance.introduction)
        instance.image = validated_data.get(
            "image", instance.image)    
        instance.password = validated_data.get("password", instance.password)
        instance.set_password(instance.password)
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()

    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_followings_count(self, obj):
        return obj.followings.count()

    class Meta:
        model = User
        fields=("id", "email", "username", "image", "gender", "date_of_birth", "preference", "introduction", "followings_count", "followers_count")


class UserMypageSerializer(serializers.ModelSerializer):
    
    posting_set = PostingSerializer(many=True)
    productreview_set = ProductReviewSerializer(many=True)
    
    class Meta:
        model = User
        fields = ("posting_set", "productreview_set")

class UserFeedSerializer(serializers.ModelSerializer):
    
    like_products = ProductListSerializer(many=True)

    class Meta:
        model = User
        fields = ("like_products", )