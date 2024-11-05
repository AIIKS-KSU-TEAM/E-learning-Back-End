from django.urls import path
from instructor.api.views import InstructorView
from courses.api.instructor.views import CourseViewSet


course_list = CourseViewSet.as_view({"get": "list", "post": "create"})

urlpatterns = [
    path("", InstructorView.as_view(), name="api-instructor"),
    path("courses/", course_list, name="api-instructor-courses-list"),
]
