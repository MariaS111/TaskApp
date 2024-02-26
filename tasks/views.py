from datetime import datetime, timezone
from pytz import timezone as pytz_timezone
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from users.permissions import IsCreator, IsInAdminsOrCreator, IsInParticipantsInAdminsOrCreator, \
    IsCreatorOrInAdminsForTask, \
    IsCreatorOrInParticipantsOrInAdminsForTask, IsCreatorOrInAdminsForCreatingTask, IsCommentOwner, CanViewComments
from .models import Task, Board, TeamBoard, Comment
from .serializers import TaskSerializer, BoardSerializer, TeamBoardSerializer, TeamTaskSerializer, CommentSerializer


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
                return TeamBoard.objects.filter(Q(project=None) & Q(Q(user=user) | Q(participants=user) | Q(admins=user))).distinct('pk')
            return TeamBoard.objects.filter(Q(project=None) & Q(pk=pk) & Q(Q(user=user) | Q(participants=user) | Q(admins=user))).distinct('pk')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == request.user:
            self.perform_destroy(instance)
            return Response({"detail": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You don't have permission to do this"}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user in instance.admins.all():
            if 'participants' in request.data and len(request.data) == 1:
                # request.data._mutable = True
                print(type(request.data['participants']))
                # request.data['participants'] = list(map(lambda x: int(x), request.data['participants'].split()))
                print(type(request.data['participants']), request.data['participants'])
                # pks = request.data.get('participants', None).split()
                # if all(get_object_or_404(CustomUser, pk=int(pk)) != instance.user and get_object_or_404(CustomUser,
                #                                                                                         pk=int(pk))
                #        not in instance.admins.all() and get_object_or_404(CustomUser, pk=int(pk))
                #        not in instance.participants.all() for pk in pks):
                # self.perform_update(instance)
                return super().partial_update(request, *args, **kwargs)
            return Response({"detail": "You don't have permission to do this"}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated(), IsInParticipantsInAdminsOrCreator()]
        elif self.action == 'update':
            return [IsAuthenticated(), IsCreator()]
        elif self.action == 'partial_update':
            return [IsAuthenticated(), IsInAdminsOrCreator()]
        return [IsAuthenticated()]


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

    def perform_update(self, serializer):
        instance = serializer.save()

        if instance.status == 'D':
            user = self.request.user
            datetime_now = str(datetime.now())[:16]
            dt = datetime.strptime(datetime_now, '%Y-%m-%d %H:%M')
            dt = dt.replace(second=0, microsecond=0)
            dt = pytz_timezone('UTC').localize(dt)

            if instance.start_date != instance.end_date and dt>instance.start_date:
                coefficient = float((dt - instance.start_date).total_seconds()) / float((instance.end_date - instance.start_date).total_seconds())
            elif dt < instance.start_date:
                first_var = -((dt - instance.start_date).total_seconds())
                coefficient = float(first_var) / float(
                    (instance.end_date - instance.start_date).total_seconds())

            new_coefficient = (user.performance_coefficient + coefficient)/2

            user.performance_coefficient = new_coefficient
            user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamTaskViewSet(ModelViewSet):
    serializer_class = TeamTaskSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        if instance.status == 'D':
            user = instance.worker
            datetime_now = str(datetime.now())[:16]
            dt = datetime.strptime(datetime_now, '%Y-%m-%d %H:%M')
            dt = dt.replace(second=0, microsecond=0)
            dt = pytz_timezone('UTC').localize(dt)

            if instance.start_date != instance.end_date and dt > instance.start_date:
                coefficient = float((dt - instance.start_date).total_seconds()) / float(
                    (instance.end_date - instance.start_date).total_seconds())
            elif dt < instance.start_date:
                first_var = -((dt - instance.start_date).total_seconds())
                print((dt - instance.start_date).total_seconds())
                print(first_var)
                print((instance.end_date - instance.start_date).total_seconds())
                coefficient = float(first_var+((instance.end_date - instance.start_date).total_seconds())) / (float(
                    (instance.end_date - instance.start_date).total_seconds()))

            new_coefficient = (user.performance_coefficient + coefficient) / 2

            user.performance_coefficient = new_coefficient
            user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            teamboards = TeamBoard.objects.filter(Q(user=user) | Q(participants=user) | Q(admins=user))
            teamboard = get_object_or_404(teamboards, pk=self.kwargs.get("teamboard_pk"))
            pk = self.kwargs.get("pk")
            if not pk:
                return teamboard.teamtask_set.exclude(status='D')
            return teamboard.teamtask_set.filter(pk=pk).exclude(status='D')

    def get_permissions(self):
        if self.action in ['retrieve', 'partial_update']:
            return [IsAuthenticated(), IsCreatorOrInParticipantsOrInAdminsForTask()]
        elif self.action == 'update':
            return [IsAuthenticated(), IsCreatorOrInAdminsForTask()]
        elif self.action == 'create':
            return [IsAuthenticated(), IsCreatorOrInAdminsForCreatingTask()]
        return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        team_board = instance.team_board
        if user == team_board.user or user in team_board.admins.all():
            self.perform_destroy(instance)
            return Response({"detail": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "You don't have permission to do this"}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        participants = instance.team_board.participants.all()
        if user in participants:
            if 'worker' in request.data and len(request.data) == 1 and int(request.data['worker']) == user.pk:
                return super().partial_update(request, *args, **kwargs)
            else:
                return Response({"detail": "You don't have permission to do this"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            if 'worker' in request.data:
                pk = request.data.get('worker', None)
                user = get_object_or_404(CustomUser, pk=pk)
                if user in participants or user in instance.team_board.admins.all() or user == instance.team_board.user:
                    return super().partial_update(request, *args, **kwargs)
                else:
                    return Response({"detail": "Invalid worker in request data"},
                                    status=status.HTTP_403_FORBIDDEN)
            return super().partial_update(request, *args, **kwargs)


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