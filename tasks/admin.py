from django.contrib import admin
from .models import Task, Board, TeamTask, TeamBoard

admin.site.register(Task)
admin.site.register(Board)
admin.site.register(TeamTask)
admin.site.register(TeamBoard)
