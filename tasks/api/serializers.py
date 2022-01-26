from rest_framework import serializers
from django.contrib.auth.models import User

from tasks.models import Task, TaskHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class TaskSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'priority', 'status', 'created_date', 'user')


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = ('task', 'old_status', 'new_status', 'changed_at')
