from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'created_at', 'user', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']
