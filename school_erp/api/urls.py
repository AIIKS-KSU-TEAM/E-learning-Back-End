from django.urls import path, include

urlpatterns = [
    path("course/", include("courses.urls")),
    path("", include("accounts.urls")),
]
