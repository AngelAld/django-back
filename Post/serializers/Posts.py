from rest_framework import serializers
from Post.models import Document, Image, Post
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


class PostCrudListSerializer(serializers.ModelSerializer):
    area = serializers.StringRelatedField(source="area.name")

    class Meta:
        model = Post
        fields = ["id", "title", "date", "published", "area"]


class PostCrudSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=False)
    documents = DocumentSerializer(many=True, read_only=False)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "date",
            "area",
            "published",
            "images",
            "documents",
        ]

    @atomic
    def create(self, validated_data):
        images = validated_data.pop("images", [])
        documents = validated_data.pop("documents", [])
        title = validated_data.get("title")
        slug = slugify(title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        slug = unique_slug
        post = Post.objects.create(**validated_data, slug=slug)

        for image in images:
            Image.objects.create(post=post, **image)

        for document in documents:
            Document.objects.create(post=post, **document)

        return post

    @atomic
    def update(self, instance, validated_data):
        images = validated_data.pop("images")
        documents = validated_data.pop("documents")
        instance.title = validated_data.get("title", instance.title)
        title = validated_data.get("title", instance.title)
        slug = slugify(title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exclude(id=instance.id).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        instance.slug = unique_slug
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
            Image.objects.create(post=instance, **image)

        for document in documents:
            Document.objects.create(post=instance, **document)
        return instance
