from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('website/about', views.about, name='about'),
    path('website/projects', views.projects, name='projects'),
    path('website/project_details/<slug:slug>/', views.project_details, name='project_details'),
    path('website/contact/', views.contact, name='contact'),
    path('website/message/', views.massage, name='message'),

]
