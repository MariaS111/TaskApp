from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Task, Board


class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = ("title", "description", "start_date", "end_date", "board")


class BoardSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = ("title", "description", "user")