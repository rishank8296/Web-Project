from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,default='unknown')
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    image = models.ImageField(upload_to='parents/')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Booking(models.Model):
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE)
    teacher = models.ForeignKey('teachers.TeacherProfile', on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)  # e.g., 10th Grade
    subject = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='bookings/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.parent.user.username} for {self.student_name}"





