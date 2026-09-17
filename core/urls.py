from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.PortalLoginView.as_view(), name='login'),
    path('logout/', views.portal_logout, name='logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
