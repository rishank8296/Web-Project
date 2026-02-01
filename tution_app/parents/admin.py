from django.contrib import admin
from .models import ParentProfile

@admin.register(ParentProfile)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_parents']

    def approve_parents(self, request, queryset):
        queryset.update(is_approved=True)
