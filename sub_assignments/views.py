# View method to create the assignment
from rest_framework import viewsets
from .models import Assignment
from .serializers import AssignmentSerializer
from django.utils import timezone

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def perform_create(self, serializer):
        # Here, 'module' refers to the instance of the Module that the assignment belongs to
        module = serializer.validated_data['module']

        # Use 'assignments' as the related name to get the latest assignment by deadline
        try:
            deadline = module.assignments.latest('deadline').deadline
        except Assignment.DoesNotExist:
            # Handle the case where there are no assignments yet (or return a default value)
            deadline = timezone.now()

        # Save the assignment with the calculated or default deadline
        serializer.save(deadline=deadline)