from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('members/', views.members, name='members'),
    path('events/', views.events, name='events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('downloads/', views.downloads, name='downloads'),
    path('contact/', views.contact, name='contact'),
    path('careers/', views.careers, name='careers'),
    path('guest-house/', views.guest_house, name='guest_house'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-portal/', views.admin_portal, name='admin_portal'),
    # Careers admin
    path('admin-portal/vacancies/', views.admin_vacancies, name='admin_vacancies'),
    path('admin-portal/vacancies/add/', views.admin_vacancy_add, name='admin_vacancy_add'),
    path('admin-portal/vacancies/<int:pk>/delete/', views.admin_vacancy_delete, name='admin_vacancy_delete'),
    path('admin-portal/vacancies/<int:pk>/toggle/', views.admin_vacancy_toggle, name='admin_vacancy_toggle'),
    # Guest house admin
    path('admin-portal/guest-house/', views.admin_guesthouse, name='admin_guesthouse'),
    path('admin-portal/guest-house/add/', views.admin_booking_add, name='admin_booking_add'),
    path('admin-portal/guest-house/<int:pk>/delete/', views.admin_booking_delete, name='admin_booking_delete'),
]
