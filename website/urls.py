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
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-portal/', views.admin_portal, name='admin_portal'),
]
