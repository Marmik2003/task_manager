import django_filters
from tasks.models import STATUS_CHOICES, Task, TaskHistory


class TaskFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)

    class Meta:
        model = Task
        fields = (
            "title",
            "status",
        )


class TaskHistoryFilter(django_filters.FilterSet):
    changed_at = django_filters.DateFilter(input_formats=['%Y-%m-%d','%d-%m-%Y'], lookup_expr='icontains')

    class Meta:
        model = TaskHistory
        fields = (
            "task",
            "old_status",
            "new_status",
            "changed_at",
        )
