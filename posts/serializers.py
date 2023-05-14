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
        if obj.content.find("br")+1:
            return obj.content.replace("<p><br></p>", "")
        if len(obj.content) > 57:
            return obj.content[:57] + "..."
        else:
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
    username = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    is_updated = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    introduction = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()

    # 2023-05-12T16:53:21.442693+09:00
    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d %H:%M")

    def get_followers_count(self, obj):
        return obj.user.followers.count()

    def get_followings_count(self, obj):
        return obj.user.followings.count()

    def get_is_updated(self, obj):
        return False if obj.created_at == obj.updated_at else True

    def get_username(self, obj):
        return obj.user.username

    def get_user_id(self, obj):
        return obj.user.id

    def get_like_count(self, obj):
        return obj.like_set.count()

    def get_user_image(self, obj):
        if obj.user.image:
            return obj.user.image
        else:
            return None

    def get_introduction(self, obj):
        return obj.user.introduction

    class Meta:
        model = Posting
        fields = (
            "user_id",
            "username",
            "title",
            "content",
            "image",
            "updated_at",
            "is_updated",
            "like_count",
            "user_image",
            "introduction",
            "followers_count",
            "followings_count",
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)


class CommentSerializer(serializers.ModelSerializer):
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
        model = Comment
        fields = (
            "username",
            "user_image",
            "content",
            "created_at",
            "updated_at",
        )
