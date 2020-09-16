from rest_framework import viewsets, permissions

from network.models import Post
from network.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_datetime")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
