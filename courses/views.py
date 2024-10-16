from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Course
from .serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class OwnerMixin(viewsets.ModelViewSet):
    def get_queryset(self):
        return Course.objects.filter(owner=self.request.user)

class OwnerEditMixin:
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CourseViewSet(OwnerMixin, OwnerEditMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_courses(self, request):
        courses = self.get_queryset()
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        subject_id = self.request.data.get('subject')
        serializer.save(owner=self.request.user, subject_id=subject_id)
