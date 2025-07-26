from django.urls import path
from . import views
from .views import student_login

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.students_list, name='students_list'),
    path('add_student/', views.add_student, name='add_student'),
    path('students/<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('students/<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),  # <-- Add this line
    path('settings/', views.settings_view, name='settings'),
    path('add_course/', views.add_course, name='add_course'),
    path('api/student_login/', student_login, name='student_login'),
]