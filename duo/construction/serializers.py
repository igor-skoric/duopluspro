from rest_framework import serializers
from .models import Project, Advance, Contact, Offer, Material, Worker,  MaterialType, Unit
from django.db.models import F, Sum, ExpressionWrapper, DecimalField, IntegerField


class ProjectSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'client', 'contact', 'start_date', 'end_date', 'status', 'status_display', 'note', 'cost']


class AdvanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Advance
        fields = ['id', 'project', 'amount', 'date', 'note', 'method']


class OfferSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'file', 'filename', 'description', 'uploaded_at', 'project']
        read_only_fields = ['uploaded_at']

    file = serializers.FileField(required=False, allow_null=True, allow_empty_file=True)

    def get_filename(self, obj):
        import os
        if obj.file and hasattr(obj.file, 'name'):
            return os.path.basename(obj.file.name)
        return ""


class MaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialType
        fields = ['id', 'name']


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']


class MaterialSerializer(serializers.ModelSerializer):
    unit_display = serializers.CharField(source='unit.name', read_only=True)
    type_display = serializers.CharField(source='type.name', read_only=True)

    class Meta:
        model = Material
        fields = [
            'id', 'project', 'type_display', 'quantity', 'unit', 'unit_display',
            'price', 'note', 'date', 'type'
        ]


class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = [
            'id', 'project', 'name', 'position', 'cost'
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    advances = AdvanceSerializer(many=True, read_only=True)
    offers = OfferSerializer(many=True, read_only=True)
    materials = MaterialSerializer(many=True, read_only=True)
    workers = WorkerSerializer(many=True, read_only=True)
    total_material_cost = serializers.SerializerMethodField()
    total_workers_cost = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    total_profit = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'client', 'contact',
            'start_date', 'end_date', 'status', 'cost', 'status_display',
            'advances', 'offers', 'materials', 'workers', 'note', 'total_material_cost', 'total_workers_cost', 'total_cost', 'total_profit'
        ]

    def get_total_material_cost(self, project):
        total = project.materials.aggregate(
            total_price=Sum(
                ExpressionWrapper(
                    F('price'),
                    output_field=IntegerField()
                )
            )
        )
        return total['total_price'] or 0

    def get_total_workers_cost(self, project):
        total = project.workers.aggregate(
            total_price=Sum(
                ExpressionWrapper(
                    F('cost'),
                    output_field=IntegerField()
                )
            )
        )
        return total['total_price'] or 0

    def get_total_cost(self, project):
        return self.get_total_material_cost(project) + self.get_total_workers_cost(project)

    def get_total_profit(self, project):
        return project.cost - self.get_total_cost(project)
