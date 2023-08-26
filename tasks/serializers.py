from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Task, Board, TeamTask, TeamBoard
from django.core.exceptions import ValidationError


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        if value:
            # return value.strftime('%Y-%m-%dT%H:%M:%S+03:00')
            return value.strftime('%Y-%m-%d %H:%M')
        return None

    def to_internal_value(self, value):
        try:
            dt = datetime.strptime(value, '%Y-%m-%d %H:%M')
            dt = dt.replace(second=0, microsecond=0)
            dt = dt + timedelta(hours=3)
            return dt
        except (ValueError, TypeError):
            raise serializers.ValidationError('Invalid datetime format')


class TaskSerializer(ModelSerializer):
    start_date = CustomDateTimeField()
    end_date = CustomDateTimeField()

    class Meta:
        model = Task
        fields = ("title", "description", "start_date", "end_date", "status")

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise ValidationError('End date must be greater than start date')

        return data

    def create(self, validated_data):
        board_pk = self.context['view'].kwargs.get('board_pk')
        validated_data['board_id'] = board_pk
        return super().create(validated_data)


class TeamTaskSerializer(ModelSerializer):
    start_date = CustomDateTimeField()
    end_date = CustomDateTimeField()

    class Meta:
        model = TeamTask
        fields = ("title", "description", "start_date", "end_date", "status", "worker")


class BoardSerializer(ModelSerializer):

    class Meta:
        model = Board
        fields = ("title", "description")

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        validated_data['user'] = user
        return super().create(validated_data)


class TeamBoardSerializer(ModelSerializer):
    class Meta:
        model = TeamBoard
        fields = ("title", "description", 'user', 'participants', 'admins')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        validated_data['user'] = user
        return super().create(validated_data)
