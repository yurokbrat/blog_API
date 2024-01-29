from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from django_filters import rest_framework as filters
from .filters import PostFilter, CommentFilter


class IsAdminOrAuthorOrReadOnly(BasePermission):
    """
       Разрешение автору и администратору изменять и удалять контент,
       а обычному пользователю только просматривать.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrAuthorOrReadOnly]
    throttle_classes = [UserRateThrottle]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter

    # Пост не проходит модерацию по умолчанию при создании или изменении
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, moderated=False)

    def perform_update(self, serializer):
        serializer.save(moderated=False)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrAuthorOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = CommentFilter

    # Комментарий не проходит модерацию по умолчанию при создании или изменении
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, moderated=False)

    def perform_update(self, serializer):
        serializer.save(moderated=False)

