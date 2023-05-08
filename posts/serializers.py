from rest_framework import serializers
from posts.models import Posting


class PostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = "__all__"
