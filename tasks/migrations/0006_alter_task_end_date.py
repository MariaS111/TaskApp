# Generated by Django 4.2.2 on 2023-08-22 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_task_end_date_alter_task_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='end_date',
            field=models.DateTimeField(),
        ),
    ]
