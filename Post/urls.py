from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AreaCRUDViewSet,
    PublicPostListViewSet,
    AreaCRUDListViewSet,
    PostCrudListViewSet,
    PublicPostDetailViewSet,
    PostCrudViewSet,
)

router = DefaultRouter()
router.register(r"admin/area", AreaCRUDViewSet, basename="area")
router.register(r"areas", AreaCRUDListViewSet, basename="areas-all")
router.register(r"posts", PublicPostListViewSet, basename="posts")
router.register(r"post", PublicPostDetailViewSet, basename="post-detail")
router.register(r"crud/posts", PostCrudListViewSet, basename="post")
router.register(r"crud/post", PostCrudViewSet, basename="post-crud")

urlpatterns = [
    path("", include(router.urls)),
]
