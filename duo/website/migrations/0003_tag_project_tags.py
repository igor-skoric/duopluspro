# Generated by Django 5.1.7 on 2025-03-20 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_project_projectimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(related_name='projects', to='website.tag'),
        ),
    ]
