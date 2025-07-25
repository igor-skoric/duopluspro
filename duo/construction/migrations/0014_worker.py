# Generated by Django 5.1.7 on 2025-07-17 07:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0013_unit_alter_material_project_alter_material_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ime')),
                ('position', models.CharField(max_length=100, verbose_name='Radno mesto')),
                ('project_rate', models.IntegerField(verbose_name='Cena rada po projektu')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workers', to='construction.project')),
            ],
        ),
    ]
