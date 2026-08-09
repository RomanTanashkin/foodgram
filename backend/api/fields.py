import base64
import binascii
from uuid import uuid4

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            try:
                header, encoded = data.split(';base64,', 1)
                extension = header.split('/')[-1].lower()
                decoded = base64.b64decode(encoded, validate=True)
            except (ValueError, binascii.Error) as exc:
                raise serializers.ValidationError(
                    'Некорректное изображение в формате Base64.'
                ) from exc
            data = ContentFile(
                decoded,
                name=f'{uuid4().hex}.{extension}',
            )
        return super().to_internal_value(data)
