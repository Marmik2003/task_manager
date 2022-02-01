from django.db import transaction
from rest_framework import generics, authentication, permissions, status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response

from tasks.models import Task, TaskHistory
from .filters import TaskFilter, TaskHistoryFilter
from .serializers import TaskSerializer, TaskHistorySerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.BasicAuthentication]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)


class TaskHistoryViewSet(ReadOnlyModelViewSet):
    serializer_class = TaskHistorySerializer
    filterset_class = TaskHistoryFilter

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.BasicAuthentication]    

    def get_queryset(self):
        return TaskHistory.objects.filter(task_id=self.kwargs['task_pk'], task__user=self.request.user).order_by('-changed_at')
