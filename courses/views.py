from rest_framework import viewsets, status
from .models import Subject, Course, Module, Content, Assignment
from .serializers import (
    SubjectSerializer,
    CourseSerializer,
    ModuleSerializer,
    ContentSerializer,
    AssignmentSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    @action(detail=True, methods=["get"], url_path="courses")
    def get_courses(self, request, pk=None):
        try:
            subject = self.get_object()
            courses = Course.objects.filter(subject=subject)
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
            return Response(
                {"detail": "Subject not found."}, status=status.HTTP_404_NOT_FOUND
            )


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["get"], url_path="modules", url_name="course-modules")
    def get_modules(self, request, pk=None):
        try:
            # Get the specific course using the primary key (pk)
            course = self.get_object()
            # Retrieve the modules related to the course
            modules = course.modules.all()
            serializer = ModuleSerializer(modules, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response(
                {"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND
            )


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get", "post"], url_path="contents")
    def get_contents(self, request, pk=None):
        """
        Custom action to retrieve or create contents for a specific module.
        Accessible at /api/modules/{moduleId}/contents/
        """
        try:
            module = self.get_object()  # Get the specific module by primary key

            if request.method == "GET":
                # Retrieve contents related to this module
                contents = module.contents.all()
                serializer = ContentSerializer(contents, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif request.method == "POST":
                # Create new content within this module
                serializer = ContentSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(module=module)  # Set the module foreign key
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Module.DoesNotExist:
            return Response(
                {"detail": "Module not found."}, status=status.HTTP_404_NOT_FOUND
            )


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom method to ensure 'module' is specified when creating a content.
        """
        module_id = self.request.data.get("module")
        if not module_id:
            raise ValidationError(
                {"module": "Module ID is required to create content."}
            )

        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            raise ValidationError({"module": "Module does not exist."})

        serializer.save(module=module)


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        module_id = self.request.data.get("module")
        try:
            module = Module.objects.get(id=module_id)
            serializer.save(module=module)
        except Module.DoesNotExist:
            raise ValidationError({"module": "Module not found."})
