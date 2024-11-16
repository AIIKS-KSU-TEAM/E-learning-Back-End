from django.contrib import admin
from .models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'created_at', 'updated_at')  
    list_filter = ('created_at', 'updated_at', 'user')  
    search_fields = ('subject', 'description', 'user__username')  

admin.site.register(Ticket, TicketAdmin)
