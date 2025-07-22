from .models import Project, Config
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from smtplib import SMTPException
from django.core.mail import send_mail
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


def home(request):
    projects = Project.objects.all()[:3]

    context = {'projects': projects}
    return render(request, 'website/pages/index.html', context)


def projects(request):
    projects = Project.objects.all()
    hide_header_footer = True
    context = {'projects': projects, 'hide_header_footer': hide_header_footer}
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


def massage(request):
    if request.method == 'POST':

        csrf_token = request.POST.get('csrfmiddlewaretoken')
        if not csrf_token:
            return JsonResponse({'error': 'CSRF token is missing'}, status=400)

        host_email = settings.DEFAULT_FROM_EMAIL

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        subject = f"Poruka sa sajta od - {name} - {phone}."

        from_email = host_email
        to_email = get_object_or_404(Config, name='email').value


        try:
            send_mail(subject, message, from_email, [to_email, 'iskoric95@gmail.com'])

            return redirect('home')
            # return JsonResponse({'message': 'Poruka je uspešno poslata!'}, status=200)

        except SMTPException as e:
            logger.error(f"SMTP greška: {e}")
            return redirect('home')

        except Exception as e:
            logger.error(f"Nešto je pošlo po zlu: {e}")
            return redirect('home')
    else:
        logger.error("error': 'Invalid request method'")
        return redirect('home')