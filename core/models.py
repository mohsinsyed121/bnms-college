from django.db import models
from django.core.validators import RegexValidator


COURSE_CHOICES = [
    ('cs', 'Computer Science'),
    ('eng', 'Engineering'),
    ('mgmt', 'Management'),
    ('comm', 'Commerce'),
    ('arts', 'Arts & Humanities'),
    ('sci', 'Applied Sciences'),
]

phone_validator = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message="Enter a valid phone number (7-15 digits, optional leading +)."
)


class StudentRegistration(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=16, validators=[phone_validator])
    dob = models.DateField(verbose_name="Date of Birth")
    course = models.CharField(max_length=10, choices=COURSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Student Registration"
        verbose_name_plural = "Student Registrations"

    def __str__(self):
        return f"{self.full_name} ({self.get_course_display()})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.subject} — {self.name}"