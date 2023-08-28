from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from .validators import validate_not_main_board
from TaskApp import settings


class TaskStatus(models.TextChoices):
    FUTURE = 'F', 'Future'
    PROGRESS = 'PR', 'In progress'
    DONE = 'D', 'Done'
    OVERDUE = 'O', 'Overdue'


class AbstractTask(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateTimeField(validators=[MinValueValidator(limit_value=timezone.now, message='Ensure this '
                                                                                                      'value is '
                                                                                                      'greater than '
                                                                                                      'or equal to '
                                                                                                      'your current '
                                                                                                      'time '
                                                                    )])
    end_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=TaskStatus.choices,
        default=TaskStatus.FUTURE,
    )

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('End date must be greater than start date')

    class Meta:
        abstract = True


class Task(AbstractTask):
    board = models.ForeignKey('Board', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['updated']


class TeamTask(AbstractTask):
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  blank=True, null=True)
    team_board = models.ForeignKey('TeamBoard', on_delete=models.CASCADE)

    def __str__(self):
        return 'TeamTask' + ' ' + self.title

    class Meta:
        verbose_name = "TeamTask"
        verbose_name_plural = "TeamTasks"
        ordering = ['updated']


class AbstractBoard(models.Model):
    title = models.CharField(max_length=30, validators=[validate_not_main_board])
    description = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)

    class Meta:
        abstract = True


class Board(AbstractBoard):

    def __str__(self):
        return self.title + ' ' + self.user.username

    class Meta:
        verbose_name = "Board"
        verbose_name_plural = "Boards"
        ordering = ['updated']


class TeamBoard(AbstractBoard):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teamboard_participants', blank=True)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teamboard_admins', blank=True)

    def __str__(self):
        return 'TeamBoard ' + self.title + ' ' + self.user.username

    class Meta:
        verbose_name = "Team Board"
        verbose_name_plural = "Team Boards"
