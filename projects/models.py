from django.db import models
from TaskApp import settings


class Project(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    watchers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='project_watchers', blank=True)


class Comment(models.Model):
    content = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team_task = models.ForeignKey("tasks.TeamTask", on_delete=models.CASCADE)
