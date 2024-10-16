from django.urls import path, include
from .views import RegisterView, login_view
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet
from . import views
from .views import LogoutView

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('teachers/count/', views.get_teacher_count, name='teacher-count'),
]
