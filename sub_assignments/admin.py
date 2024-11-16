from django.contrib import admin
from .models import Assignment

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'created_at') 
    search_fields = ('title',)

admin.site.register(Assignment, AssignmentAdmin)
