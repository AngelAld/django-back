from rest_framework.serializers import ModelSerializer, StringRelatedField
from Post.models import Image


class ImageSerializer(ModelSerializer):
    url = StringRelatedField(read_only=True)

    class Meta:
        model = Image
        fields = ["id", "url", "is_cover"]
