from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course
from .serializers import CourseSerializer
from django.urls import reverse_lazy
from rest_framework import generics
from rest_framework import permissions


# Define custom permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a course to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the course.
        return obj.owner == request.user

class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerCourseMixin(OwnerMixin, generics.GenericAPIView):
    serializer_class = CourseSerializer
    permission_classes = []  # Allow access to anyone, including unauthenticated users

class ManageCourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    permission_classes = []  # Allow access to anyone, including unauthenticated users

class CourseCreateView(OwnerCourseMixin, generics.CreateAPIView):
    queryset = Course.objects.all()
    permission_classes = []  # Allow access to anyone, including unauthenticated users

class CourseUpdateView(OwnerCourseMixin, generics.UpdateAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsOwnerOrReadOnly]  # Allow read access to anyone, but only the owner can edit

class CourseDeleteView(OwnerCourseMixin, generics.DestroyAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsOwnerOrReadOnly]  # Allow read access to anyone, but only the owner can delete

class ManageCourseListView(APIView):
    def get(self, request, format=None):
        courses = Course.objects.all()  # Allow access to all courses
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
