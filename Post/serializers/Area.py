from rest_framework import serializers
from Post.models import Area
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            "id",
            "name",
        ]


class AreaSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField(source="group.name", read_only=True)

    class Meta:
        model = Area
        fields = "__all__"


class AreaEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"
