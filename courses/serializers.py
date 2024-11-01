from rest_framework import serializers
from .models import Subject, Course, Module, Content

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'title', 'description', 'created']

    def create(self, validated_data):
        owner = self.context['request'].user
        
        validated_data.pop('owner', None)  
        
        course = Course.objects.create(owner=owner, **validated_data)
        return course


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'content_type', 'content']