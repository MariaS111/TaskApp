from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Task, Board
from .serializers import TaskSerializer, BoardSerializer


class BoardViewSet(ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        user = self.request.user
        queryset = user.board_set.all()
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = self.request.user
        queryset = user.board_set.all()
        board = get_object_or_404(queryset, pk=pk)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    # def get_queryset(self):
    #     user = self.request.user
    #     pk = self.kwargs.get("pk")
    #     if not pk:
    #         return user.board_set.all()
    #     return user.board_set.get(pk=pk)
    def destroy(self, request, pk=None):
        user = self.request.user
        queryset = user.board_set.all()
        board = get_object_or_404(queryset, pk=pk)
        if board.title == "Main board":
            return Response({"detail": "Cannot delete the main board."}, status=status.HTTP_403_FORBIDDEN)
        else:
            board.delete()
        return Response({"success: Board deleted"})


# class TaskViewSet(ModelViewSet):
#     serializer_class = TaskSerializer
#     permission_classes = (IsAuthenticated, )

    # def get_queryset(self):
    #     user = self.request.user
    #     pk = self.kwargs.get("pk")
    #     if not pk:
    #         return user.task_set.all()
    #     return user.task_set.filter(pk=pk)

    # @action(methods=['get'], detail=True)
    # def board(self, request, pk=None):
    #     boards = Board.objects.all()
    #     return Response({'boards': [c.title for c in boards]})


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


# class TaskApiView(ListCreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#
#
# class TaskApiGet(RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer



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
