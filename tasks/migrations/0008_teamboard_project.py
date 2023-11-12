# Generated by Django 4.2.2 on 2023-11-12 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('tasks', '0007_alter_board_user_alter_teamboard_admins_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamboard',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
    ]
