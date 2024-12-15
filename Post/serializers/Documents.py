import io
from rest_framework import serializers
from Post.models import Document
from drf_extra_fields.fields import Base64FileField
import PyPDF2


class PDFBase64File(Base64FileField):
    ALLOWED_TYPES = ["pdf"]

    def get_file_extension(self, filename, decoded_file):
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(decoded_file))
            if reader.is_encrypted:
                raise serializers.ValidationError("Archivo PDF está encriptado")
        except PyPDF2.errors.PdfReadError:
            raise serializers.ValidationError("Archivo PDF inválido")
        else:
            return "pdf"


class DocumentSerializer(serializers.ModelSerializer):
    document = PDFBase64File()

    class Meta:
        model = Document
        fields = [
            "title",
            "document",
        ]
