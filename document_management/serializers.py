from rest_framework import serializers
from .models import Document

class DocumentUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Document
        fields = ['title', 'type', 'file', 'assigned_to']

    def create(self, validated_data):
        raw_file = validated_data.pop('file').read()
        from .utils import encrypt_file_content
        validated_data['file_encrypted'] = encrypt_file_content(raw_file)
        validated_data['submitted_by'] = self.context['request'].user
        return Document.objects.create(**validated_data)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'type', 'status', 'submitted_by', 'created_at']
