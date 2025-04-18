# Generated by Django 5.1.5 on 2025-03-28 08:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_date', models.DateField(auto_now_add=True)),
                ('dropped', models.BooleanField(default=False)),
                ('dropped_date', models.DateField(blank=True, null=True)),
                ('class_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.class')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignments.student')),
            ],
            options={
                'unique_together': {('student', 'class_instance', 'semester')},
            },
        ),
    ]
