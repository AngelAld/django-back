from rest_framework.viewsets import ModelViewSet
from Post.models import Area, Post
from Post.serializers.Posts import (
    PostAllSerializer,
    PostCrudListSerializer,
    PostDetailSerializer,
    PostCrudSerializer,
)
from Post.serializers.Area import AreaEditSerializer, AreaSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)


class PostAreaFilter(filters.FilterSet):
    area = filters.CharFilter(field_name="area__name")


class PublicPostDetailViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostDetailSerializer
    http_method_names = ["get"]
    filter_backends = [filters.DjangoFilterBackend]
    lookup_field = "slug"


class PublicPostListViewSet(ListModelMixin, GenericViewSet):
    queryset = Post.objects.filter(published=True)
    serializer_class = PostAllSerializer
    http_method_names = ["get"]
    filter_backends = [filters.DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostAreaFilter
    pagination_class = LimitOffsetPagination
    ordering = ("-date",)
    ordering_fields = ("date", "title")
    search_fields = ["title", "content"]


class AreaCRUDListViewSet(ListModelMixin, GenericViewSet):
    queryset = Area.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = AreaSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    search_fields = ["name", "description"]
    http_method_names = ["get"]


class AreaCRUDViewSet(
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Area.objects.all()
    serializer_class = AreaEditSerializer
    http_method_names = ["get", "post", "put", "delete"]


class PostCrudListViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostCrudListSerializer
    http_method_names = ["get"]
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    pagination_class = LimitOffsetPagination
    filterset_fields = ["area"]
    search_fields = ["title", "content"]


class PostCrudViewSet(
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostCrudSerializer
    http_method_names = ["get", "post", "put", "delete"]
