from rest_framework import viewsets, status
from courses.models import Course
from courses.serializers import CourseSerializer, ModuleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        # The instructor
        user = self.request.user

        # Filter the courses by the current instructor
        
        qs = super().get_queryset()

        return qs

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
