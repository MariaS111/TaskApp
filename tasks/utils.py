from django.utils import timezone
from .models import Task, TaskStatus


class Util:
    @staticmethod
    def check_deadlines():
        now = timezone.now()
        overdue_tasks = Task.objects.filter(end_date__lt=now, status=TaskStatus.PROGRESS)
        for task in overdue_tasks:
            task.status = TaskStatus.OVERDUE
            task.save()
        return f"{len(overdue_tasks)} tasks marked as overdue"

    @staticmethod
    def check_task_is_in_progress():
        now = timezone.now()
        progress_tasks = Task.objects.filter(start_date__lt=now, status=TaskStatus.FUTURE)
        for task in progress_tasks:
            task.status = TaskStatus.PROGRESS
            task.save()
        return f"{len(progress_tasks)} tasks marked as in progress"
