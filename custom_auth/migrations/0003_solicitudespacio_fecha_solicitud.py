# Generated by Django 5.1.5 on 2025-01-24 13:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0002_espaciofisico_solicitudespacio'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudespacio',
            name='fecha_solicitud',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
