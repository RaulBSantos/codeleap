from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from network.models import Post
from network.serializers import PostSerializer
from network.permissions import IsOwner


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_datetime")
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]
