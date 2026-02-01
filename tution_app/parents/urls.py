from django.urls import path
from . import views
from tution_app.teachers.views import teacher_home

urlpatterns = [
    # PUBLIC
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='parent_register'),
    path('logout/', views.logout, name='logout'),

    # DASHBOARDS
    path('dashboard/home/', views.admin_home, name='admin_home'),
    path('parent/home/', views.parent_home, name='parent_home'),
    path('teacher/home/', teacher_home, name='teacher_home'),

    # ADMIN
    path('dashboard/admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('dashboard/admin/approvals/', views.admin_approvals, name='admin_approvals'),

    # BOOKINGS
    path('booking/approve/<int:id>/', views.approve_booking, name='approve_booking'),
    path('booking/reject/<int:id>/', views.reject_booking, name='reject_booking'),

    # TEACHER APPROVALS
    path('teacher/approve/<int:id>/', views.approve_teacher, name='approve_teacher'),
    path('teacher/reject/<int:id>/', views.reject_teacher, name='reject_teacher'),

    # PARENT APPROVALS
    path('parent/approve/<int:id>/', views.approve_parent, name='approve_parent'),
    path('parent/reject/<int:id>/', views.reject_parent, name='reject_parent'),
    path('parent/delete/<int:id>/', views.reject_parent, name='delete_parent'),
]
