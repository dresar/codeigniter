from django.urls import path
from . import views

app_name = 'invitation_templates'

urlpatterns = [
    path('', views.template_list, name='template_list'),
    path('create/', views.template_create, name='template_create'),
    path('<int:pk>/edit/', views.template_edit, name='template_edit'),
    path('<int:pk>/delete/', views.template_delete, name='template_delete'),
    path('<int:pk>/preview/', views.template_preview, name='template_preview'),
    path('css/<int:pk>/delete/', views.delete_css_file, name='delete_css_file'),
    path('js/<int:pk>/delete/', views.delete_js_file, name='delete_js_file'),
    path('image/<int:pk>/delete/', views.delete_image_file, name='delete_image_file'),
]

