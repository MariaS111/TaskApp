from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Task, Board


class TaskSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = ("title", "description", "start_date", "end_date")

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('End date must be greater than start date')
        return data

    def create(self, validated_data):
        board_pk = self.context['view'].kwargs.get('board_pk')
        validated_data['board_id'] = board_pk
        return super().create(validated_data)


class BoardSerializer(ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = ("title", "description")

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        validated_data['user'] = user
        return super().create(validated_data)