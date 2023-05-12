from rest_framework import serializers
from posts.models import Posting, Comment


class PostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = (
            "title",
            "content",
            "image",
        )


class PostingListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if len(obj.content) > 57:
            return obj.content[:57] + "..."
        return obj.content

    def get_username(self, obj):
        return obj.user.username

    def get_user_image(self, obj):
        if obj.user.image:
            return obj.user.image
        else:
            return None

    def get_like_count(self, obj):
        return obj.like_set.count()

    def get_comment_count(self, obj):
        return obj.comment_set.count()

    class Meta:
        model = Posting
        fields = (
            "id",
            "title",
            "content",
            "image",
            "username",
            "like_count",
            "comment_count",
            "user_image",
        )


class PostingCreateSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_user_image(self, obj):
        if obj.user.image:
            return obj.user.image
        else:
            return None

    class Meta:
        model = Posting
        fields = (
            "title",
            "content",
            "username",
            "user_image",
        )


class PostingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = (
            "title",
            "content",
            "image",
            "created_at",
            "updated_at",
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "content",
            "created_at",
            "updated_at",
        )
