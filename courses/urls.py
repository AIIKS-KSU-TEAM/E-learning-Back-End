from django.urls import path
from . import views

urlpatterns = [
    # Endpoint to manage courses for the logged-in user
    path('mine/', 
         views.ManageCourseListView.as_view(), 
         name='manage_course_list'),
    
    # Endpoint to create a new course
    path('create/', 
         views.CourseCreateView.as_view(), 
         name='course_create'),
    
    # Endpoint to edit a specific course identified by its primary key (pk)
    path('<int:pk>/edit/', 
         views.CourseUpdateView.as_view(), 
         name='course_edit'),
    
    # Endpoint to delete a specific course identified by its primary key (pk)
    path('<int:pk>/delete/', 
         views.CourseDeleteView.as_view(), 
         name='course_delete'),
]
