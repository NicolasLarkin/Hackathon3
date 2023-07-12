from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from functools import wraps

from comment.serializers import CommentSerializer
# from comment.serializers import CommentSerializer
from like.models import Favorite
from like.serializers import LikeUserSerializer
from .models import Post
from . import serializers
from .permissions import IsAuthor, IsAuthorOrAdmin
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class StandardResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = StandardResultPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title', 'body')
    filterset_fields = ('owner', 'category',)

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        return serializers.PostDetailSerializer

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthorOrAdmin(), ]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthor(), ]
        return [permissions.IsAuthenticatedOrReadOnly(), ]

    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(instance=comments, many=True)
        return Response(serializer.data, status=200)

    # @method_decorator(cache_page(60 * 60 * 2))
    @action(['POST'], detail=True)
    def likes(self):
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikeUserSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    # @method_decorator(cache_page(60 * 60 * 2))
    @action(['POST', 'DELETE'], detail=True)
    def favorites(self, request, pk):
        post = self.get_object()
        user = request.user
        favorite = user.favorites.filter(post=post)
        if request.method == 'POST':
            if user.favorites.exists():
                return Response({'msg': 'Already in Favorite'})
            Favorite.objects.create(owner=user, post=post)
            return Response({'msg': 'Added to favorites'}, status=201)
        if favorite.exists():
            favorite.delete()
            return Response({'msg', 'Deleted From Favorite'}, status=204)
        return Response({'msg': 'Post Not Found in Favorite'}, status=404)
