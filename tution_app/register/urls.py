from django.urls import path
from . import views

urlpatterns = [
    path('add_student/', views.add_student, name='add_student'),
    path('book_teacher/', views.book_teacher, name='book_teacher'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
]
