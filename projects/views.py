from django.db.models import Q
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from projects.models import Project
from projects.serializers import ProjectSerializer
from tasks.models import TeamBoard
from tasks.views import TeamBoardViewSet
from users.permissions import IsCreator, IsInWatchersOrCreator


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


class ProjectTeamBoardViewSet(TeamBoardViewSet):
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            pk = self.kwargs.get("pk")
            project = self.kwargs.get("project_pk")
            if not pk:
                return TeamBoard.objects.filter(Q(project=project) & Q(Q(user=user) | Q(participants=user) | Q(admins=user))).distinct('pk')
            return TeamBoard.objects.filter(Q(project=project) & Q(pk=pk) & Q(Q(user=user) | Q(participants=user) | Q(admins=user))).distinct('pk')
