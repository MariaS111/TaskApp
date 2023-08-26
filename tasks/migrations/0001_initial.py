# Generated by Django 4.2.2 on 2023-08-26 19:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tasks.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, validators=[tasks.validators.validate_not_main_board])),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Board',
                'verbose_name_plural': 'Boards',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('start_date', models.DateTimeField(validators=[django.core.validators.MinValueValidator(limit_value=django.utils.timezone.now, message='Ensure this value is greater than or equal to your current time ')])),
                ('end_date', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('F', 'Future'), ('PR', 'In progress'), ('D', 'Done'), ('O', 'Overdue')], default='F', max_length=2)),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'ordering': ['updated'],
            },
        ),
        migrations.CreateModel(
            name='TeamBoard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, validators=[tasks.validators.validate_not_main_board])),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Team Board',
                'verbose_name_plural': 'Team Boards',
            },
        ),
        migrations.CreateModel(
            name='TeamTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('start_date', models.DateTimeField(validators=[django.core.validators.MinValueValidator(limit_value=django.utils.timezone.now, message='Ensure this value is greater than or equal to your current time ')])),
                ('end_date', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('F', 'Future'), ('PR', 'In progress'), ('D', 'Done'), ('O', 'Overdue')], default='F', max_length=2)),
                ('team_board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.teamboard')),
            ],
            options={
                'verbose_name': 'TeamTask',
                'verbose_name_plural': 'TeamTasks',
                'ordering': ['updated'],
            },
        ),
    ]
