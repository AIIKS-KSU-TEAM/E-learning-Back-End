from rest_framework import serializers
from .models import Course, Content, Text, Video, Image, File, Module
from django.contrib.contenttypes.models import ContentType


# Serializer for Text content
class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['id', 'content', 'created', 'updated']  # Adjust based on your Text model


# Serializer for Video content
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'url', 'created', 'updated']  # Adjust based on your Video model


# Serializer for Image content
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'created', 'updated']  # Adjust based on your Image model


# Serializer for File content
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'created', 'updated']  # Adjust based on your File model


# Content Serializer - For handling all types of content
class ContentSerializer(serializers.ModelSerializer):
    # Nested serializers for each content type
    text = TextSerializer(read_only=True)
    video = VideoSerializer(read_only=True)
    image = ImageSerializer(read_only=True)
    file = FileSerializer(read_only=True)

    class Meta:
        model = Content
        fields = ['id', 'course', 'module', 'content_type', 'object_id', 'text', 'video', 'image', 'file', 'created', 'updated']
        read_only_fields = ['content_type', 'object_id', 'created', 'updated']


# Serializer for the Course model
class CourseSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'created', 'owner', 'contents']  # Removed 'updated' if not needed
        read_only_fields = ['owner', 'created']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class CustomContentSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=32)
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    file = serializers.FileField(required=False)
    url = serializers.URLField(required=False)

    def __init__(self, instance=None, data=None, user=None, module=None, **kwargs):
        self.module = module
        self.user = user
        super().__init__(instance, data, **kwargs)

    def save(self, **kwargs):

        validated_data = self.validated_data

        type = validated_data.get("type")

        content = None

        if type == "text":

            title = validated_data.get("title")
            content = validated_data.get("content")
            # Create text
            text = Text.objects.create(title=title, content=content, owner=self.user)

            content_type = ContentType.objects.get_for_model(text)
            # Create content type save
            content = Content.objects.create(module=self.module, content_type=content_type, object_id=text.id)


        return content

class ModuleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Module
        fields = ["id", "course", "title", "description", "order"]
        read_only_fields = ["id", "course"]