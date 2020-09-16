from django.contrib.auth.models import User
from rest_framework import serializers
from network.models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
        ]


class PostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Post
        fields = ["id", "user", "username", "created_datetime", "title", "content"]
