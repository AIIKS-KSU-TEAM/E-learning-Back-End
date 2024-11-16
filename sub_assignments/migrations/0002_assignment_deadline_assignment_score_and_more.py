# Generated by Django 5.1.2 on 2024-11-11 13:14

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_assignment_module'),
        ('sub_assignments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='assignment',
            name='score',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='courses.module'),
        ),
    ]