from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Task, Board
from .serializers import TaskSerializer, BoardSerializer


class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        self.get_permissions()
        user = self.request.user
        if self.request.user.is_authenticated:
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

# @api_view(['GET'])
# def get_routes(request):
#     routes = [
#         {
#             'Endpoint': 'api/tasks/',
#             'method': 'GET',
#             'body': None,
#             'description': 'Returns an array of tasks'
#         },
#         {
#             'Endpoint': 'api/tasks/id',
#             'method': 'GET',
#             'body': None,
#             'description': 'Returns a single task object'
#         },
#         {
#             'Endpoint': 'api/tasks/create/',
#             'method': 'POST',
#             'body': {'body': ""},
#             'description': 'Creates new task with data sent in post request'
#         },
#         {
#             'Endpoint': 'api/tasks/id/update/',
#             'method': 'PUT',
#             'body': {'body': ""},
#             'description': 'Creates an existing task with data sent in post request'
#         },
#         {
#             'Endpoint': 'api/tasks/id/delete/',
#             'method': 'DELETE',
#             'body': None,
#             'description': 'Deletes and exiting task'
#         },
#     ]
#     return Response(routes)

# class TaskApiView(APIView):
#     def get(self, request):
#         tasks = Task.objects.all()
#         return Response({'tasks': TaskSerializer(tasks, many=True).data})
#
#     def post(self, request):
#         serializer = TaskSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'task': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": 'Method PUT is not allowed'})
#         try:
#             instance = Task.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#         serializer = TaskSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"task": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": 'Method DELETE is not allowed'})
#         try:
#             instance = Task.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#         instance.delete()
#         return Response({"task": "delete task" + str(pk)})
