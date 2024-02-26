import math

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from projects.models import Project
from projects.serializers import ProjectSerializer
from tasks.models import TeamBoard, TeamTask
from tasks.views import TeamBoardViewSet, TeamTaskViewSet
from users.permissions import IsCreator, IsInWatchersOrCreator
from rest_framework.decorators import action
from datetime import timedelta


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            pk = self.kwargs.get("pk")
            if not pk:
                return Project.objects.filter(Q(user=user) | Q(watchers__in=[user])).distinct('pk')
            return Project.objects.filter(Q(pk=pk) & Q(user=user) | Q(watchers__in=[user])).distinct('pk')

    def get_permissions(self):
        if self.action in ['retrieve']:
            return [IsAuthenticated(), IsInWatchersOrCreator()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsCreator()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['GET'], url_path='report')
    def project_report(self, request, pk=None):
        project = self.get_object()

        board_count = project.teamboard_set.count()
        task_count = TeamTask.objects.filter(team_board__project=project).count()
        completed_task_count = TeamTask.objects.filter(team_board__project=project, status='D').count()
        participants_count = project.watchers.count()

        if task_count > 0:
            completion_percentage = (completed_task_count / task_count) * 100
        else:
            completion_percentage = 0

        report_data = {
            'board_count': board_count,
            'task_count': task_count,
            'completed_task_count': completed_task_count,
            'completion_percentage': completion_percentage,
            'participants_count': participants_count,
        }

        return Response(report_data, status=status.HTTP_200_OK)


class ProjectTeamBoardViewSet(TeamBoardViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            pk = self.kwargs.get("pk")
            project = self.kwargs.get("project_pk")
            if not pk:
                return TeamBoard.objects.filter(Q(project=project) & Q(Q(user=user) | Q(participants=user) | Q(admins=user))).distinct('pk')
            return TeamBoard.objects.filter(Q(project=project) & Q(pk=pk) & Q(Q(user=user) | Q(participants=user) | Q(admins=user))).distinct('pk')


class ProjectTeamTaskViewSet(TeamTaskViewSet):
    @action(detail=True, methods=['GET'], url_path='expected_completion_date')
    def calculate_expected_completion_date(self, request, project_pk, teamboard_pk, pk=None):
        instance = self.get_object()
        user = instance.worker
        coefficient = user.performance_coefficient

        start_date = instance.start_date
        end_date = instance.end_date

        if coefficient > 1:
            all_seconds = (end_date - start_date).total_seconds() * coefficient
            expected_completion_date = start_date - timedelta(seconds=math.ceil(all_seconds))
        elif 0 < coefficient < 1:
            expected_completion_date = start_date + timedelta(
                seconds=(end_date - start_date).total_seconds() / coefficient)

        return Response({"expected_completion_date": expected_completion_date}, status=status.HTTP_200_OK)

