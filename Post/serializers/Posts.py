from rest_framework import serializers
from Post.models import Post
from Post.serializers.Documents import DocumentSerializer
from Post.serializers.Images import ImageSerializer
from django.db.transaction import atomic
from django.utils.text import slugify

# not authenticated serializers


class PostAllSerializer(serializers.ModelSerializer):
    area = serializers.StringRelatedField(source="area.name")

    class Meta:
        model = Post
        fields = ["id", "slug", "title", "cover", "content", "date", "area"]


class PostDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    area = serializers.StringRelatedField(source="area.name")

    class Meta:
        model = Post
        fields = [
            "id",
            "slug",
            "title",
            "content",
            "cover",
            "date",
            "area",
            "images",
            "documents",
        ]


# authenticated serializers


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "slug",
            "title",
            "content",
            "date",
            "area",
            "published",
            "cover",
            "images",
            "documents",
        ]
        read_only_fields = ["slug"]

    @atomic
    def create(self, validated_data):
        images = validated_data.pop("images")
        documents = validated_data.pop("documents")
        title = validated_data.get("title")
        slug = slugify(title)
        post = Post.objects.create(**validated_data, slug=slug)
        for image in images:
            ImageSerializer.create(ImageSerializer(), image, post)
        for document in documents:
            DocumentSerializer.create(DocumentSerializer(), document, post)
        return post

    @atomic
    def update(self, instance, validated_data):
        images = validated_data.pop("images")
        documents = validated_data.pop("documents")
        instance.title = validated_data.get("title", instance.title)
        instance.slug = slugify(instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.area = validated_data.get("area", instance.area)
        instance.date = validated_data.get("date", instance.date)
        instance.published = validated_data.get("published", instance.published)
        instance.save()
        # Delete old files
        instance.images.all().delete()
        instance.documents.all().delete()
        # Create new files
        for image in images:
            ImageSerializer.create(ImageSerializer(), image, instance)
        for document in documents:
            DocumentSerializer.create(DocumentSerializer(), document, instance)
        return instance
