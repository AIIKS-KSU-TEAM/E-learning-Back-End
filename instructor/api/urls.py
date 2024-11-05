from django.urls import path
from instructor.api.views import InstructorView

urlpatterns = [
    path("", InstructorView.as_view(), name="api-instructor"),
]
