# BNMS College — Demo Django Website

A complete Django web application for a demo college site: public marketing pages, a
student registration form, a contact form, and a single login portal that routes
students and staff to different dashboards.

## Project layout

```
bnms_college_project/
├── manage.py
├── requirements.txt
├── bnms_college/          # Project config (settings, root urls)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/                  # The app: models, forms, views, admin, urls
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── admin.py
│   ├── urls.py
│   └── migrations/
├── templates/              # All HTML templates (Tailwind CSS via CDN)
│   ├── base.html
│   ├── home.html
│   ├── about.html
│   ├── register.html
│   ├── contact.html
│   ├── login.html
│   ├── student_dashboard.html
│   └── admin_dashboard.html
└── static/
    └── css/style.css        # Design tokens / small helper styles
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser   # create a staff/admin account
python manage.py runserver
```

Visit **http://127.0.0.1:8000/**.

Django's built-in admin (for raw data editing) lives at `/django-admin/`, kept
separate from the app's own `/admin/dashboard/` staff dashboard.

## Pages & routes

| URL                       | Purpose                                                            |
|---------------------------|----------------------------------------------------------------------|
| `/`                       | Home — hero, highlights, admissions call to action                 |
| `/about/`                 | About Us — history, mission, vision                                |
| `/register/`              | Student registration form → saves to `StudentRegistration`         |
| `/contact/`                | Contact form → saves to `ContactMessage`                            |
| `/login/`                  | Single login page for students **and** staff                       |
| `/student/dashboard/`      | Student dashboard (requires login) — shows the student's own record |
| `/admin/dashboard/`        | Staff/admin dashboard (requires `is_staff`/`is_superuser`) — shows all registrations & inquiries |
| `/django-admin/`           | Django's built-in admin site                                       |

## Role-based login

`PortalLoginView` (in `core/views.py`) is a single `LoginForm`-backed view. After
authentication it checks `user.is_staff` / `user.is_superuser`:

- **Staff/superuser** → redirected to `/admin/dashboard/`, which lists every
  `StudentRegistration` and `ContactMessage` in sortable tables.
- **Regular user (student)** → redirected to `/student/dashboard/`, which shows any
  `StudentRegistration` rows whose email matches the logged-in user's account email.

`/admin/dashboard/` is protected with `@user_passes_test` so a student account cannot
view it directly (they're bounced back to `/login/`).

## Included demo data

This project ships with a pre-populated `db.sqlite3` so you can try it immediately
without any setup:

| Role    | Username   | Password       | Lands on              |
|---------|------------|----------------|------------------------|
| Admin   | `admin`    | `admin12345`   | `/admin/dashboard/`    |
| Student | `student1` | `student12345` | `/student/dashboard/`  |

It also includes one sample `StudentRegistration` and one sample `ContactMessage` so
the admin dashboard isn't empty on first look. Delete `db.sqlite3` and re-run
`python manage.py migrate` for a clean slate — **change these passwords (or delete
the users) before deploying anywhere real.**

## Creating demo users

```bash
python manage.py createsuperuser        # staff/admin account
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_user('student1', 'student1@example.com', 'yourpassword')"
```

A student's dashboard matches on **email**, so make sure the student's registration
form email matches the account email you create for them.

## Notes

- Styling uses Tailwind CSS via CDN (`base.html`) plus a small `static/css/style.css`
  for a couple of custom tokens (color variables, table rules) that Tailwind's
  utility classes don't cover directly. No build step required.
- Database is SQLite (`db.sqlite3`), created automatically on first `migrate`.
- Forms use Django's `ModelForm` with server-side validation (email format, phone
  pattern, required fields) and Tailwind-styled widgets.
- This is a demo/education project — for production use you'd want HTTPS enforcement,
  environment-based secrets, a production database, and stronger password policies.
