from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ContentViewSet, ModuleViewset, CourseModuleViewset
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'modules', ModuleViewset, basename='module')
router.register(r'contents', ContentViewSet, basename='content')

modules_list = CourseModuleViewset.as_view({
    "get": "list",
    "post": "create",
})

modules_detail = CourseModuleViewset.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('modules/<int:pk>/content/', views.ModuleContentView.as_view(), name='module-content'),
    path("courses/<int:course_id>/modules/", modules_list, name="course-module-list"),
    path("courses/<int:course_id>/modules/<int:module_id>/", modules_detail, name="course-module-detail"),
]
