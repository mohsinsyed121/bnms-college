from django.contrib import admin
from .models import StudentRegistration, ContactMessage


@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'course', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('full_name', 'email', 'phone')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'submitted_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('submitted_at',)
