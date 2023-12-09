from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from users.permissions import IsCommentOwner, CanViewComments
from .serializers import CommentSerializer
from .models import Comment


class ProjectViewSet(ModelViewSet):
    pass


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'destroy']:
            return [IsCommentOwner()]
        else:
            return [IsAuthenticated(), CanViewComments()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, team_task_id=self.kwargs['teamtask_pk'])

    def get_queryset(self):
        team_task_pk = self.kwargs['teamtask_pk']
        return Comment.objects.filter(team_task_id=team_task_pk)