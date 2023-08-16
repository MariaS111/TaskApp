from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Task


class TaskSerializer(ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ("title", "description", "start_date", "end_date", "board", "user")
