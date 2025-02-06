from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.transaction import atomic
from django.contrib.auth.password_validation import validate_password


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            "id",
            "name",
        ]


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    group_ids = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
    )
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "groups",
            "group_ids",
        ]

    @atomic
    def create(self, validated_data):
        password = validated_data.pop("password")
        if not password:
            raise ValidationError("Password is required")
        validate_password(password)
        user: User = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    @atomic
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            validate_password(password)
            instance.set_password(password)
            instance.save()
        return super().update(instance, validated_data)
