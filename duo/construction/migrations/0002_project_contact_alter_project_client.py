# Generated by Django 5.1.7 on 2025-07-15 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='contact',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='client',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
