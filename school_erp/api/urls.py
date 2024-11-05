from django.urls import path, include

urlpatterns = [
    path("course/", include("courses.urls")),
    path("instructor/", include("instructor.api.urls")),
    path("", include("accounts.urls")),
]
