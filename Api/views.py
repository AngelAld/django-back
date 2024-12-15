from rest_framework.viewsets import ModelViewSet
from Api.serializers import LoginSerializer
from Post.models import Area, Post
from Post.serializers.Posts import (
    PostAllSerializer,
    PostCrudListSerializer,
    PostDetailSerializer,
    PostCrudSerializer,
)
from Post.serializers.Area import AreaEditSerializer, AreaSerializer, GroupSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth.models import Group

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
    permission_classes = [IsAuthenticated]
    serializer_class = AreaSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name", "description"]
    http_method_names = ["get", "delete"]


# authenticated views


class GroupViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ["get"]


class AreaViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Area.objects.all()
    serializer_class = AreaEditSerializer
    http_method_names = ["get", "post", "put", "delete"]


class PostCrudListViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostCrudListSerializer
    http_method_names = ["get", "delete"]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = LimitOffsetPagination
    filterset_fields = ["area"]
    search_fields = ["title", "content"]


class PostCrudViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostCrudSerializer
    http_method_names = ["get", "post", "put", "delete"]


class LoginView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    http_method_names = ["post"]
