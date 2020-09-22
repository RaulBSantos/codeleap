from rest_framework import viewsets, permissions
from rest_framework.response import Response

from network.models import Post
from network.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_datetime")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        queryset = Post.objects.filter(user=user).order_by("-created_datetime")
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
