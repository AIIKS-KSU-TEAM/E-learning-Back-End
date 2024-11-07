from django.contrib import admin
from .models import Subject, Course, Module, Content


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "owner", "created")
    search_fields = ("title", "description")


class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "course")


class ContentAdmin(admin.ModelAdmin):
    list_display = ("content_type", "module")
    search_fields = ("content",)


# Register models with custom admin configurations
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Content, ContentAdmin)
