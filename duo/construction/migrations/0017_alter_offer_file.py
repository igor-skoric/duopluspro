# Generated by Django 5.1.7 on 2025-07-22 13:14

import construction.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0016_project_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=construction.utils.offer_upload_path),
        ),
    ]
