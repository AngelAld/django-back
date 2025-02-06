from rest_framework.viewsets import ModelViewSet
from Auth.serializers import LoginSerializer
from django.contrib.auth.models import User


class LoginView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    http_method_names = ["post"]
