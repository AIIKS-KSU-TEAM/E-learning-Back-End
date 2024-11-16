from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogoutView, LoginView, RegisterView, TeacherViewSet, UserProfileView
from .views import ChangePasswordView

router = DefaultRouter()
router.register(r"teachers", TeacherViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="user-profile"), 
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("", include(router.urls)),
]
