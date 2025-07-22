from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Project, Advance, Offer, Material, MaterialType, Unit, Worker
from .serializers import ProjectSerializer, ProjectDetailSerializer, AdvanceSerializer, OfferSerializer, \
    MaterialSerializer, MaterialTypeSerializer, UnitSerializer, WorkerSerializer


def app(request):
    context = {}
    return render(request, 'construction/pages/app.html', context)


def single_project(request, pk):
    context = {}
    return render(request, 'construction/pages/single_project.html', context)


# Paginacija
class ProjectPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProjectListView(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-start_date')
    serializer_class = ProjectSerializer

    # Dodaj search i pagination
    pagination_class = ProjectPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'client', 'note']  # zameni poljima koja želiš da pretražuješ


class ProjectDetailAPIView(RetrieveAPIView):
    queryset = Project.objects.prefetch_related('advances', 'offers', 'materials', 'workers').all()
    serializer_class = ProjectDetailSerializer


class AdvanceViewSet(viewsets.ModelViewSet):
    queryset = Advance.objects.all()
    serializer_class = AdvanceSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class MaterialTypeViewSet(viewsets.ModelViewSet):
    queryset = MaterialType.objects.all()
    serializer_class = MaterialTypeSerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer