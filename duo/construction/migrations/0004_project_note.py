# Generated by Django 5.1.7 on 2025-07-15 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0003_project_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='note',
            field=models.TextField(blank=True),
        ),
    ]
