from django.db.models import Case, IntegerField, When
from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Project, Advance, Offer, Material, MaterialType, Unit, Worker
from .serializers import ProjectSerializer, ProjectDetailSerializer, AdvanceSerializer, OfferSerializer, \
    MaterialSerializer, MaterialTypeSerializer, UnitSerializer, WorkerSerializer
from django.contrib.auth.decorators import login_required


@login_required(login_url='/admin/login/')
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
    """Lista projekata: aktivni prvi, završeni poslednji; filteri ?status= & ?client="""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = ProjectPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "client", "contact", "note"]

    def get_queryset(self):
        qs = Project.objects.annotate(
            _status_order=Case(
                When(status="active", then=0),
                When(status="planned", then=1),
                When(status="paused", then=2),
                When(status="cancelled", then=3),
                When(status="completed", then=4),
                default=5,
                output_field=IntegerField(),
            )
        ).order_by("_status_order", "-start_date", "name")

        status = self.request.query_params.get("status", "").strip()
        if status:
            qs = qs.filter(status=status)

        return qs


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