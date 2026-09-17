from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_POST

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


def _dashboard_context(reg_form_override=None, reg_override_pk=None,
                        msg_form_override=None, msg_override_pk=None):
    """Builds the context for admin_dashboard.html, including a bound
    ModelForm per row so each row's edit modal is pre-filled. If a save
    attempt just failed validation, that one row's form is swapped for the
    invalid (error-carrying) form and its modal is flagged to auto-open."""
    registrations = StudentRegistration.objects.all()
    inquiries = ContactMessage.objects.all()

    reg_rows = []
    for r in registrations:
        form = reg_form_override if (reg_override_pk == r.pk and reg_form_override) \
            else StudentRegistrationForm(instance=r)
        reg_rows.append({'obj': r, 'form': form})

    msg_rows = []
    for m in inquiries:
        form = msg_form_override if (msg_override_pk == m.pk and msg_form_override) \
            else ContactMessageForm(instance=m)
        msg_rows.append({'obj': m, 'form': form})

    return {
        'registrations': registrations,
        'inquiries': inquiries,
        'reg_rows': reg_rows,
        'msg_rows': msg_rows,
        'open_registration_modal': reg_override_pk,
        'open_message_modal': msg_override_pk,
    }


@user_passes_test(_staff_check, login_url='login')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html', _dashboard_context())


# ---- Admin-only management actions: review toggle, edit, delete ----

@user_passes_test(_staff_check, login_url='login')
@require_POST
def toggle_registration_reviewed(request, pk):
    r = get_object_or_404(StudentRegistration, pk=pk)
    r.is_reviewed = not r.is_reviewed
    r.save(update_fields=['is_reviewed'])
    messages.success(request, f"Marked {r.full_name} as {'reviewed' if r.is_reviewed else 'not reviewed'}.")
    return redirect('admin_dashboard')


@user_passes_test(_staff_check, login_url='login')
@require_POST
def edit_registration(request, pk):
    r = get_object_or_404(StudentRegistration, pk=pk)
    form = StudentRegistrationForm(request.POST, instance=r)
    if form.is_valid():
        form.save()
        messages.success(request, f"Updated registration for {r.full_name}.")
        return redirect('admin_dashboard')
    messages.error(request, "Please fix the errors in the registration form.")
    return render(request, 'admin_dashboard.html',
                  _dashboard_context(reg_form_override=form, reg_override_pk=pk))


@user_passes_test(_staff_check, login_url='login')
@require_POST
def delete_registration(request, pk):
    r = get_object_or_404(StudentRegistration, pk=pk)
    name = r.full_name
    r.delete()
    messages.success(request, f"Deleted registration for {name}.")
    return redirect('admin_dashboard')


@user_passes_test(_staff_check, login_url='login')
@require_POST
def toggle_message_reviewed(request, pk):
    m = get_object_or_404(ContactMessage, pk=pk)
    m.is_reviewed = not m.is_reviewed
    m.save(update_fields=['is_reviewed'])
    messages.success(request, f"Marked message from {m.name} as {'reviewed' if m.is_reviewed else 'not reviewed'}.")
    return redirect('admin_dashboard')


@user_passes_test(_staff_check, login_url='login')
@require_POST
def edit_message(request, pk):
    m = get_object_or_404(ContactMessage, pk=pk)
    form = ContactMessageForm(request.POST, instance=m)
    if form.is_valid():
        form.save()
        messages.success(request, f"Updated message from {m.name}.")
        return redirect('admin_dashboard')
    messages.error(request, "Please fix the errors in the message form.")
    return render(request, 'admin_dashboard.html',
                  _dashboard_context(msg_form_override=form, msg_override_pk=pk))


@user_passes_test(_staff_check, login_url='login')
@require_POST
def delete_message(request, pk):
    m = get_object_or_404(ContactMessage, pk=pk)
    name = m.name
    m.delete()
    messages.success(request, f"Deleted message from {name}.")
    return redirect('admin_dashboard')
