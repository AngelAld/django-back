from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Api.views import (
    AreaViewSet,
    PostAllViewSet,
    AreaAllViewSet,
    PostCrudListViewSet,
    PostOneViewSet,
    PostCrudViewSet,
    LoginView,
    GroupViewSet,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()

router.register(r"areas", AreaViewSet, basename="area")
router.register(r"areas-list", AreaAllViewSet, basename="areas-all")
router.register(r"posts", PostAllViewSet, basename="posts")
router.register(r"post-detail", PostOneViewSet, basename="post-detail")
router.register(r"post-crud-list", PostCrudListViewSet, basename="post")
router.register(r"post-crud", PostCrudViewSet, basename="post-crud")
router.register(r"login", LoginView, basename="login")
router.register(r"groups", GroupViewSet, basename="group")
urlpatterns = [
    path("", include(router.urls)),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
