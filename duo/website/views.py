from .models import Project
from django.shortcuts import render, get_object_or_404


def home(request):
    projects = Project.objects.all()[:3]

    context = {'projects': projects}
    return render(request, 'website/pages/index.html', context)


def projects(request):
    projects = Project.objects.all()

    context = {'projects': projects}
    return render(request, 'website/pages/projects.html', context)


def project_details(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'website/pages/project_details.html', {'project': project})


def contact(request):
    context = {}
    return render(request, 'website/pages/contact.html', context)


def about(request):
    context = {}
    return render(request, 'website/pages/about.html', context)