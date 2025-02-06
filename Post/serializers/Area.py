from rest_framework import serializers
from Post.models import Area


class AreaSerializer(serializers.ModelSerializer):
    group = serializers.StringRelatedField(source="group.name", read_only=True)

    class Meta:
        model = Area
        fields = "__all__"


class AreaEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = "__all__"
