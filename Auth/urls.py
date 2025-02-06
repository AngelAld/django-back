from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Auth.views import (
    LoginView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()

router.register(r"login", LoginView, basename="login")
urlpatterns = [
    path("auth/", include(router.urls)),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
