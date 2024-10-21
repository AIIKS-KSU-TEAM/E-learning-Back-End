from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet
from . import views
from accounts.views import LogoutView, LoginView,RegisterView

router = DefaultRouter()
router.register(r"teachers", TeacherViewSet)

urlpatterns = [
    path("teachers/count/", views.get_teacher_count, name="teacher-count"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
]
