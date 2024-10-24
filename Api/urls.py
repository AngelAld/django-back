from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Api.views import AreaViewSet, PostAllViewSet, AreaAllViewSet, PostOneViewSet, PostViewSet


router = DefaultRouter()

router.register(r"areas", AreaViewSet, basename="area")
router.register(r"areas-all", AreaAllViewSet, basename="areas-all")
router.register(r"posts", PostAllViewSet, basename="posts")
router.register(r"post-detail", PostOneViewSet, basename="post-detail")
router.register(r"post", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]
