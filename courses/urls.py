from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, CourseViewSet, ModuleViewSet, ContentViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'contents', ContentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
