from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCreator, IsInAdminsOrCreator, IsInParticipantsInAdminsOrCreator
from .models import Task, Board, TeamBoard
from .serializers import TaskSerializer, BoardSerializer, TeamBoardSerializer, TeamTaskSerializer


class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            pk = self.kwargs.get("pk")
            if not pk:
                return user.board_set.all()
            return user.board_set.filter(pk=pk)

    def destroy(self, request, *args, **kwargs):
        board = self.get_object()
        if board.title == "Main board":
            return Response({"detail": "Cannot delete the main board."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['GET'])
    def done_tasks(self, request, pk=None):
        board = self.get_object()
        done_tasks = board.task_set.filter(status='D')
        serializer = TaskSerializer(done_tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='done_tasks/(?P<task_pk>[^/.]+)')
    def done_task(self, request, pk=None, task_pk=None):
        board = self.get_object()
        task = board.task_set.get(pk=task_pk, status='D')
        if task:
            serializer = TaskSerializer(task, many=False)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class TeamBoardViewSet(ModelViewSet):
    serializer_class = TeamBoardSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            pk = self.kwargs.get("pk")
            if not pk:
                return TeamBoard.objects.filter(Q(user=user) | Q(participants=user) | Q(admins=user))
            return TeamBoard.objects.filter(Q(pk=pk) & Q(Q(user=user) | Q(participants=user) | Q(admins=user)))

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            permission_classes = [IsAuthenticated, IsInParticipantsInAdminsOrCreator]
        elif self.action == 'delete':
            permission_classes = [IsAuthenticated, IsCreator]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsInAdminsOrCreator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            board = get_object_or_404(Board, pk=self.kwargs.get("board_pk"))
            pk = self.kwargs.get("pk")
            if not pk:
                return board.task_set.exclude(status='D')
            return board.task_set.filter(pk=pk).exclude(status='D')


class TeamTaskViewSet(ModelViewSet):
    serializer_class = TeamTaskSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            teamboard = get_object_or_404(TeamBoard, pk=self.kwargs.get("teamboard_pk"))
            pk = self.kwargs.get("pk")
            if not pk:
                return teamboard.teamtask_set.exclude(status='D')
            return teamboard.teamtask_set.filter(pk=pk).exclude(status='D')

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthenticated, ]
        return [permission() for permission in permission_classes]

    def partial_update(self, request, *args, **kwargs):
        pass
