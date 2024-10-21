from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Course, Content, Text, Video, Image, File, Module
from .serializers import CourseSerializer, ContentSerializer, CustomContentSerializer, ModuleSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class ModuleContentView(APIView):
    def post(self, request, pk, format=None):
        module = get_object_or_404(Module, pk=pk)

        serializer = CustomContentSerializer(data=request.data, user=request.user, module=module)

        if serializer.is_valid():

            serializer.save()

            return Response({'message': 'Content added successfully!'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors)



class CourseContentView(APIView):
    def post(self, request, pk, format=None):
        module = get_object_or_404(Module, pk=pk)

        serializer = ContentSerializer(data=request.data, user=request.user, module=module)

        if serializer.is_valid():

            serializer.save()

            return Response({'message': 'Content added successfully!'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors)
    
    def get(self, request, pk, format=None):
        course = get_object_or_404(Course, pk=pk)
        
        contents = Content.objects.filter(course=course)  
        content_data = [{"id": content.id, "title": content.title, "description": content.description} for content in contents]

        return Response(content_data, status=status.HTTP_200_OK)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class OwnerMixin(viewsets.ModelViewSet):
    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)

# Course ViewSet
class CourseViewSet(OwnerMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_courses(self, request):
        courses = self.get_queryset()
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data
        content_type_id = data.get('content_type')
        object_id = data.get('object_id')
        
        content_type = ContentType.objects.get(id=content_type_id)
        model_class = content_type.model_class()
        
        item = model_class.objects.get(id=object_id)
        content = Content.objects.create(
            owner=request.user,
            module_id=data.get('module'),
            content_type=content_type,
            object_id=object_id,
            item=item
        )
        
        serializer = self.get_serializer(content)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ModuleViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    
# /course/courses/<int:pk>/modules/
class CourseModuleViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()

        course = get_object_or_404(Course, pk=self.kwargs.get("course_id", None))

        qs = qs.filter(course=course)

        return qs