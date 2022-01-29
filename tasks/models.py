from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


STATUS_CHOICES = (
    ("PENDING", "Pending"),
    ("IN_PROGRESS", "In Progress"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
)


class TaskHistory(models.Model):
    version = models.PositiveIntegerField(editable=False)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    new_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    changed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-version',)
        unique_together = ('version', 'task')
        
    def save(self, *args, **kwargs):
        current_version = TaskHistory.objects.filter(task=self.task).order_by('-version').first()
        self.version = current_version.version + 1 if current_version else 1
        super(TaskHistory, self).save(*args, **kwargs)


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def summary_history(self):
        return TaskHistory.objects.filter(task=self).order_by('-version')

    def save(self, *args, **kwargs):
        super(Task, self).save(*args, **kwargs)
        summary_history = self.summary_history()
        if not summary_history.exists():
            TaskHistory.objects.create(task=self, old_status='', new_status='PENDING')
        if summary_history.first().new_status != self.status:
            TaskHistory.objects.create(task=self, old_status=summary_history.first().new_status, new_status=self.status)


class UserTaskReportSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    report_time = models.TimeField(default=timezone.now, null=True, blank=True)
