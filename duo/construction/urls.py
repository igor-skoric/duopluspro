from django.contrib import admin
from django.urls import path, include
from . import views
from . import api_urls


urlpatterns = [
    path('app/', views.app, name='app'),
    path('statistika/', views.statistics, name='statistika'),
    path('odjava/', views.construction_logout, name='construction_logout'),
    path('single_project/<int:pk>', views.single_project, name='single_project'),
    path('api/', include(api_urls)),
]
