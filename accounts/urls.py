from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import LogoutView, LoginView, RegisterView, TeacherViewSet

router = DefaultRouter()
router.register(r"teachers", TeacherViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("", include(router.urls)),
]
