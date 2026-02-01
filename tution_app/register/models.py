from django.db import models
from tution_app.parents.models import ParentProfile

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    school = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='registrations/', null=True, blank=True)

    class Meta:
        app_label = 'register'

    def __str__(self):
        return self.name
