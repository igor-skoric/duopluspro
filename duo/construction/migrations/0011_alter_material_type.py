# Generated by Django 5.1.7 on 2025-07-15 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0010_alter_material_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='construction.materialtype'),
        ),
    ]
