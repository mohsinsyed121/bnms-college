from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .forms import StudentRegistrationForm, ContactMessageForm, PortalLoginForm
from .models import StudentRegistration, ContactMessage


def home(request):
    highlights = [
        {
            'title': 'NAAC A+ Accredited',
            'desc': 'Recognised for academic excellence and institutional quality.',
        },
        {
            'title': '40+ Years of Legacy',
            'desc': 'Shaping graduates across science, commerce, arts and management.',
        },
        {
            'title': '95% Placement Rate',
            'desc': 'Strong industry partnerships connect students to careers early.',
        },
        {
            'title': '6 Undergraduate Schools',
            'desc': 'Computer Science, Engineering, Management, Commerce, Arts, Sciences.',
        },
    ]
    return render(request, 'home.html', {'highlights': highlights})


def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Registration successful! Our admissions team will contact you shortly."
            )
            return redirect('register')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thanks for reaching out! We'll get back to you within 2 business days."
            )
            return redirect('contact')
    else:
        form = ContactMessageForm()
    return render(request, 'contact.html', {'form': form})


class PortalLoginView(LoginView):
    """A single login page with role-based redirection after authentication."""
    template_name = 'login.html'
    authentication_form = PortalLoginForm
    redirect_authenticated_user = False

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')


def portal_logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def student_dashboard(request):
    # A student sees their own registration record(s) matched by their account email.
    my_records = StudentRegistration.objects.filter(email__iexact=request.user.email) \
        if request.user.email else StudentRegistration.objects.none()
    return render(request, 'student_dashboard.html', {'my_records': my_records})


def _staff_check(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(_staff_check, login_url='login')
def admin_dashboard(request):
    registrations = StudentRegistration.objects.all()
    inquiries = ContactMessage.objects.all()
    return render(request, 'admin_dashboard.html', {
        'registrations': registrations,
        'inquiries': inquiries,
    })
