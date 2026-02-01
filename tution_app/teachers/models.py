from django.db import models
from django.contrib.auth.models import User

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    subject = models.CharField(max_length=50)
    experience = models.IntegerField(default=0)
    image = models.ImageField(upload_to='teacher_images/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
