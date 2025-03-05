# Generated by Django 5.1.5 on 2025-02-25 03:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_professor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfessorClassSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_number', models.IntegerField(blank=True, null=True)),
                ('class_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.class')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profclassect', to='courses.professor')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.semester')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='professors',
            field=models.ManyToManyField(through='courses.ProfessorClassSection', to='courses.professor'),
        ),
    ]
