from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from posts.models import Post, Group, Comment, User
from .serializers import (
    PostSerializer, GroupSerializer,
    CommentSerializer, UserSerializer
)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        
        if post and self.kwargs['post_id']:
            serializer.save(
                author=self.request.user,
                post_id=self.kwargs['post_id']
            )
