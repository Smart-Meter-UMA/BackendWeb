# Generated by Django 3.2.8 on 2023-05-12 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estadistica',
            name='fechaMaxDiaKw',
        ),
        migrations.RemoveField(
            model_name='estadistica',
            name='fechaMaxMesKw',
        ),
        migrations.RemoveField(
            model_name='estadistica',
            name='fechaMinDiaKw',
        ),
        migrations.RemoveField(
            model_name='estadistica',
            name='fechaMinMesKw',
        ),
        migrations.RemoveField(
            model_name='estadistica',
            name='maxDiaKw',
        ),
        migrations.RemoveField(
            model_name='estadistica',
            name='maxMesKw',
        ),
        migrations.RemoveField(
            model_name='estadistica',
            name='minDiaKw',
        ),
        migrations.RemoveField(
            model_name='estadistica',
            name='minMesKw',
        ),
    ]
