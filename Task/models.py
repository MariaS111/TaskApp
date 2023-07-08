from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['updated']


class Board(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"