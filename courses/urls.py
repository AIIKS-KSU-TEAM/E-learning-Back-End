from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import SubjectViewSet, CourseViewSet, ModuleViewSet, ContentViewSet, AssignmentViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'contents', ContentViewSet)

modules_router = NestedSimpleRouter(router, r'modules', lookup='module')
modules_router.register(r'assignments', AssignmentViewSet, basename='module-assignments')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(modules_router.urls)),  
]
