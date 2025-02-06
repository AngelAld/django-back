from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAdminUser
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "post", "put", "delete"]


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "post", "put", "delete"]
