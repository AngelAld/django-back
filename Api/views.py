from rest_framework.viewsets import ModelViewSet
from Post.models import Area, Post
from Post.serializers.Posts import (
    PostAllSerializer,
    PostDetailSerializer,
    PostSerializer,
)
from Post.serializers.Area import AreaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

# not authenticated views


class PostAreaFilter(filters.FilterSet):
    area = filters.CharFilter(field_name="area__name")


class PostOneViewSet(ModelViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostDetailSerializer
    http_method_names = ["get"]
    filter_backends = [DjangoFilterBackend]
    lookup_field = "slug"


class PostAllViewSet(ModelViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostAllSerializer
    http_method_names = ["get"]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostAreaFilter
    pagination_class = LimitOffsetPagination
    ordering = ("-date",)
    ordering_fields = ("date", "title")
    search_fields = ["title", "content"]


class AreaAllViewSet(ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    http_method_names = ["get"]


# authenticated views
class AreaViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    http_method_names = ["post", "put", "delete"]


class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    http_method_names = ["get", "post", "put", "delete"]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PostAreaFilter
    search_fields = ["title", "content"]
