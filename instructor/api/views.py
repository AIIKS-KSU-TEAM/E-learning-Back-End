from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response


class InstructorView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self):

        return Response(
            {
                "message": "Welcome insctructore",
                "todo": "Check and return dashboard details about an instructor",
            }
        )
