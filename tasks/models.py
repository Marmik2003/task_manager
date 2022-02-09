from django.db import models, transaction
from django.utils import timezone
from django.contrib.auth.models import User


STATUS_CHOICES = (
    ("PENDING", "Pending"),
    ("IN_PROGRESS", "In Progress"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
)


class TaskHistory(models.Model):
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    new_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    changed_at = models.DateTimeField(auto_now=True)


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
        return TaskHistory.objects.filter(task=self).order_by('-changed_at')

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.status == "COMPLETED":
            super().save(*args, **kwargs)
            return
        _priority = self.priority
        tasks = Task.objects.filter(
            user=self.user,
            priority__gte=_priority,
            deleted=False
        ).exclude(id=self.id).select_for_update().order_by('priority')
        updating_tasks = []
        for task in tasks:
            if task.priority > _priority:
                break
            _priority = task.priority = task.priority + 1
            updating_tasks.append(task)
        Task.objects.bulk_update(updating_tasks, ['priority'])

        super(Task, self).save(*args, **kwargs)
        
        summary_history = self.summary_history()
        if not summary_history.exists():
            TaskHistory.objects.create(task=self, old_status='', new_status=self.status)
        if summary_history.first().new_status != self.status:
            TaskHistory.objects.create(task=self, old_status=summary_history.first().new_status, new_status=self.status)


class UserTaskReportSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    report_time = models.TimeField(default=timezone.now, null=True, blank=True)
    last_sent_at = models.DateTimeField()

    def save(self):
        if self.last_sent_at is None:
            self.last_sent_at = timezone.now() + timezone.timedelta(days=-1, hours=self.report_time.hour, minutes=self.report_time.minute)
        super(UserTaskReportSetting, self).save()
