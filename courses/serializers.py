from rest_framework import serializers
from .models import Subject, Course, Module, Content

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['subject', 'title', 'description']  # Specify expected fields

    def create(self, validated_data):
        # Extract the owner from the context (request.user)
        owner = self.context['request'].user
        
        # Remove 'owner' from validated_data if it exists
        validated_data.pop('owner', None)  # Ensure no owner key is passed
        
        # Save the course with the owner automatically assigned
        course = Course.objects.create(owner=owner, **validated_data)
        return course


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
