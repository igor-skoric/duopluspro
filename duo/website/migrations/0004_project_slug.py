# Generated by Django 5.1.7 on 2025-03-21 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_tag_project_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
