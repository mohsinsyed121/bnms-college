from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import StudentRegistration, ContactMessage


TEXT_INPUT_CLASSES = (
    "w-full rounded-md border border-slate-300 bg-white px-4 py-2.5 text-sm "
    "text-slate-800 placeholder-slate-400 focus:border-[#1B2A4A] focus:outline-none "
    "focus:ring-2 focus:ring-[#1B2A4A]/20 transition"
)


class StudentRegistrationForm(forms.ModelForm):
    dob = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': TEXT_INPUT_CLASSES})
    )

    class Meta:
        model = StudentRegistration
        fields = ['full_name', 'email', 'phone', 'dob', 'course']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': TEXT_INPUT_CLASSES, 'placeholder': 'e.g. Ananya Sharma'
            }),
            'email': forms.EmailInput(attrs={
                'class': TEXT_INPUT_CLASSES, 'placeholder': 'you@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': TEXT_INPUT_CLASSES, 'placeholder': '+91 9876543210'
            }),
            'course': forms.Select(attrs={'class': TEXT_INPUT_CLASSES}),
        }
        labels = {
            'full_name': 'Full name',
            'dob': 'Date of birth',
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': TEXT_INPUT_CLASSES, 'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': TEXT_INPUT_CLASSES, 'placeholder': 'you@example.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': TEXT_INPUT_CLASSES, 'placeholder': 'How can we help?'
            }),
            'message': forms.Textarea(attrs={
                'class': TEXT_INPUT_CLASSES, 'placeholder': 'Write your message...',
                'rows': 5
            }),
        }


class PortalLoginForm(AuthenticationForm):
    """Single login form used by both students and staff/admin.
    Role separation happens in the view based on user.is_staff."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': TEXT_INPUT_CLASSES, 'placeholder': 'Username', 'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': TEXT_INPUT_CLASSES, 'placeholder': 'Password'
        })
    )
