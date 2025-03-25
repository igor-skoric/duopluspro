from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('projects', views.projects, name='projects'),
    path('project_details/<slug:slug>/', views.project_details, name='project_details'),
    path('contact/', views.contact, name='contact')

]
