from django.db import models
from TaskApp import settings


class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    board = models.ForeignKey('Board', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['updated']


class Board(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' ' + self.user.username

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        ordering = ['updated']