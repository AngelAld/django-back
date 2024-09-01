from rest_framework.serializers import ModelSerializer, StringRelatedField
from Post.models import Document


class DocumentSerializer(ModelSerializer):
    url = StringRelatedField(read_only=True)

    class Meta:
        model = Document
        fields = ["id", "title", "url"]
