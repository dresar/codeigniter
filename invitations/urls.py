from django.urls import path
from . import views

app_name = 'invitations'

urlpatterns = [
    # Home
    path('', views.home_view, name='home'),
    
    # Auth URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Invitation CRUD
    path('invitation/create/', views.invitation_create, name='invitation_create'),
    path('invitation/<int:pk>/edit/', views.invitation_edit, name='invitation_detail_edit'),
    path('invitation/<int:pk>/delete/', views.invitation_delete, name='invitation_delete'),
    
    # Gallery Management
    path('invitation/<int:invitation_pk>/gallery/add/', views.gallery_add, name='gallery_add'),
    path('gallery/<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),
    
    # Guest Management
    path('invitation/<int:invitation_pk>/guest/add/', views.guest_add, name='guest_add'),
    path('guest/<int:pk>/delete/', views.guest_delete, name='guest_delete'),
    
    # Public URLs
    path('wedding/<slug:slug>/', views.invitation_public, name='invitation_detail'),
    path('wedding/<slug:slug>/checkin/', views.checkin_view, name='checkin'),
    path('wedding/<slug:slug>/rsvp/', views.rsvp_submit, name='rsvp_submit'),
]

