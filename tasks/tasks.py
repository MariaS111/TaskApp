from celery import shared_task
from .utils import Util


@shared_task()
def check_task_deadlines():
    return Util.check_deadlines()


@shared_task()
def check_task_is_started():
    return Util.check_task_is_in_progress()
