from django.contrib import admin

# Register your models here.

from .models import TeacherProfile

@admin.register(TeacherProfile)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone', 'subject', 'experience')
    list_filter = ('subject', 'gender')
    search_fields = ('name', 'email', 'subject')
