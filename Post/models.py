from django.db import models
from django.contrib.auth.models import Group


def image_upload(instance, filename):
    return f"images/{instance.post.title}/{filename}"


def document_upload(instance, filename):
    return f"documents/{instance.post.title}/{filename}"


class Area(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    content = models.TextField()
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField()
    published = models.BooleanField(default=False)

    @property
    def cover(self):
        cover = Image.objects.filter(post=self, is_cover=True).first()
        if cover:
            return cover.image.url
        return None

    def __str__(self):
        return self.title


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=image_upload)
    is_cover = models.BooleanField(default=False)

    @property
    def url(self):
        return self.image.url

    def __str__(self):
        return self.image.name


class Document(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="documents")
    title = models.CharField(max_length=100)
    document = models.FileField(upload_to=document_upload)

    @property
    def url(self):
        return self.document.url

    def __str__(self):
        return self.title
