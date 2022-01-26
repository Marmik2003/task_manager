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

    def _save_task(self, task):
        task_id = task.validated_data.get('id', None)
        _priority = task.validated_data.get('priority', None)
        tasks = Task.objects.filter(
            user=self.request.user,
            priority__gte=_priority,
            deleted=False
        ).exclude(id=task_id).select_for_update().order_by('priority')
        updating_tasks = []
        with transaction.atomic():  
            while tasks.exists() and tasks.first().priority == _priority:
                task1 = tasks[0]
                task1.priority += 1
                updating_tasks.append(task1)
                _priority += 1
                print(updating_tasks)
            Task.objects.bulk_update(updating_tasks, ['priority'])
            task.save(user=self.request.user)
    
    def perform_create(self, serializer):
        self._save_task(serializer)

    def perform_update(self, serializer):
        self._save_task(serializer)


class TaskHistoryViewSet(ReadOnlyModelViewSet):
    serializer_class = TaskHistorySerializer
    filterset_class = TaskHistoryFilter

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.BasicAuthentication]    

    def get_queryset(self):
        return TaskHistory.objects.filter(task_id=self.kwargs['task_pk']).order_by('-version')
