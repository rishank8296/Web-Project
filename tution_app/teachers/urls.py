from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.teacher_register, name='teacher_register'),
    path('pending/', views.pending_teacher, name='pending_teacher'),
    path('teacher/approve/<int:id>/', views.approve_teacher, name='approve_teacher'),
    path('teacher/reject/<int:id>/', views.reject_teacher, name='reject_teacher'),
    path('teacher/delete/<int:id>/', views.delete_teacher, name='delete_teacher'),
    path('students/', views.teacher_students, name='teacher_students'),
]
