from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.views import LoginView

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
    my_records = (
        StudentRegistration.objects.filter(
            email__iexact=request.user.email
        )
        if request.user.email
        else StudentRegistration.objects.none()
    )

    return render(
        request,
        'student_dashboard.html',
        {'my_records': my_records}
    )


def _staff_check(user):
    return user.is_authenticated and (
        user.is_staff or user.is_superuser
    )


@user_passes_test(_staff_check, login_url='login')
def admin_dashboard(request):
    registrations = StudentRegistration.objects.all()
    inquiries = ContactMessage.objects.all()

    return render(
        request,
        'admin_dashboard.html',
        {
            'registrations': registrations,
            'inquiries': inquiries,
        }
    )


@login_required
@user_passes_test(_staff_check, login_url='login')
def edit_student(request, id):
    student = get_object_or_404(StudentRegistration, id=id)

    if request.method == 'POST':
        form = StudentRegistrationForm(
            request.POST,
            instance=student
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Student record updated successfully."
            )
            return redirect('admin_dashboard')
    else:
        form = StudentRegistrationForm(instance=student)

    return render(
        request,
        'edit_student.html',
        {
            'form': form,
            'student': student,
        }
    )


@login_required
@user_passes_test(_staff_check, login_url='login')
def delete_student(request, id):
    student = get_object_or_404(StudentRegistration, id=id)

    if request.method == 'POST':
        student.delete()
        messages.success(
            request,
            "Student record deleted successfully."
        )
        return redirect('admin_dashboard')

    return render(
        request,
        'delete_student.html',
        {'student': student}
    )


@login_required
@user_passes_test(_staff_check, login_url='login')
def approve_student(request, id):
    student = get_object_or_404(StudentRegistration, id=id)

    if request.method == 'POST':
        student.approved = not student.approved
        student.save()

        if student.approved:
            messages.success(
                request,
                "Student approved successfully."
            )
        else:
            messages.info(
                request,
                "Student approval removed."
            )

    return redirect('admin_dashboard')