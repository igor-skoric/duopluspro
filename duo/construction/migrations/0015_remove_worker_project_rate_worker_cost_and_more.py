# Generated by Django 5.1.7 on 2025-07-17 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0014_worker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='project_rate',
        ),
        migrations.AddField(
            model_name='worker',
            name='cost',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='worker',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='worker',
            name='position',
            field=models.CharField(max_length=100),
        ),
    ]
