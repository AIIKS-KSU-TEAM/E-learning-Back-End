from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, CourseViewSet, ModuleViewSet, ContentViewSet, AssignmentViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'contents', ContentViewSet)
router.register(r'assignments', AssignmentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('modules/<int:module_id>/', include(router.urls)),

]
