from django.conf import settings
from django.contrib.auth import logout
from django.db.models import Case, IntegerField, Sum, When
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Project, Advance, Offer, Material, MaterialType, Unit, Worker
from .serializers import ProjectSerializer, ProjectDetailSerializer, AdvanceSerializer, OfferSerializer, \
    MaterialSerializer, MaterialTypeSerializer, UnitSerializer, WorkerSerializer
from django.contrib.auth.decorators import login_required


def _fmt_rsd_amount(value):
    n = int(value or 0)
    return f"{n:,}".replace(",", "\u00a0")


@login_required(login_url='/admin/login/')
def app(request):
    context = {}
    return render(request, 'construction/pages/app.html', context)


@login_required(login_url='/admin/login/')
def single_project(request, pk):
    context = {}
    return render(request, 'construction/pages/single_project.html', context)


@login_required(login_url='/admin/login/')
def statistics(request):
    total_projects = Project.objects.count()

    contract_sum = Project.objects.aggregate(s=Sum("cost"))["s"] or 0
    advances_sum = Advance.objects.aggregate(s=Sum("amount"))["s"] or 0
    materials_sum = Material.objects.aggregate(s=Sum("price"))["s"] or 0
    workers_sum = Worker.objects.aggregate(s=Sum("cost"))["s"] or 0
    expenses_sum = materials_sum + workers_sum
    surplus = contract_sum - expenses_sum

    advance_pct = round((advances_sum / contract_sum) * 100, 1) if contract_sum else 0.0
    expense_pct = round((expenses_sum / contract_sum) * 100, 1) if contract_sum else 0.0

    status_rows = []
    for key, label in Project.STATUS_CHOICES:
        c = Project.objects.filter(status=key).count()
        pct = round((c / total_projects) * 100, 1) if total_projects else 0.0
        status_rows.append({"key": key, "label": label, "count": c, "pct": pct})

    top_qs = Project.objects.order_by("-cost", "name")[:10]
    top_projects = [
        {"id": p.id, "name": p.name, "client": p.client, "cost_fmt": _fmt_rsd_amount(p.cost)}
        for p in top_qs
    ]

    context = {
        "total_projects": total_projects,
        "contract_fmt": _fmt_rsd_amount(contract_sum),
        "advances_fmt": _fmt_rsd_amount(advances_sum),
        "materials_fmt": _fmt_rsd_amount(materials_sum),
        "workers_fmt": _fmt_rsd_amount(workers_sum),
        "expenses_fmt": _fmt_rsd_amount(expenses_sum),
        "surplus_fmt": _fmt_rsd_amount(surplus),
        "advance_pct": advance_pct,
        "expense_pct": expense_pct,
        "status_rows": status_rows,
        "top_projects": top_projects,
    }
    return render(request, "construction/pages/statistics.html", context)


@require_POST
def construction_logout(request):
    logout(request)
    return redirect(settings.LOGIN_URL)


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