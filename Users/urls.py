from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Users.views import UserViewSet, GroupViewSet as UsersGroupViewSet

router = DefaultRouter()


router.register(r"admin/users", UserViewSet, basename="user")
router.register(r"admin/groups", UsersGroupViewSet, basename="admin-group")
urlpatterns = [
    path("", include(router.urls)),
]
