from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    deleted_at = serializers.DateTimeField(
        read_only=True, required=False, help_text="This field is automatically populated with the current date and time when the category is deleted.")

    class Meta:
        model = Product
        fields = '__all__'

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
