from rest_framework.serializers import ModelSerializer
from Post.models import Image
from drf_extra_fields.fields import Base64ImageField


class ImageSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Image
        fields = ["image", "is_cover"]
