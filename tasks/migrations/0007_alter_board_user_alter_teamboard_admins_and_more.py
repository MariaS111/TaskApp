# Generated by Django 4.2.2 on 2023-08-27 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0006_alter_teamtask_worker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teamboard',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='teamboard_admins', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teamboard',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='teamboard_participants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='teamboard',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
