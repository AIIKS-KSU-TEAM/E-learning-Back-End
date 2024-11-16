from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ticket
from .serializers import TicketSerializer
from rest_framework.permissions import IsAuthenticated

class TicketCreateView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        user = request.user
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

