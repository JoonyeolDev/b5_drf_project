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


class PostingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = (
            "title",
            "content",
            "image",
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
