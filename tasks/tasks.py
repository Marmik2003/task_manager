from .models import UserTaskReportSetting, Task
import datetime
from django.utils import timezone
from celery.decorators import periodic_task
from task_manager.celery import app

from django.core.mail import send_mail


@periodic_task(run_every=datetime.timedelta(minutes=1))
def send_email_reports():
    for user in UserTaskReportSetting.objects.all():
        k_start = timezone.now().replace(tzinfo=None)
        k_end = datetime.datetime.combine(timezone.now().date(), user.report_time, tzinfo=None)
        k = (k_end - k_start).total_seconds()
        if k < 60:
            pending_tasks = Task.objects.filter(user=user.user, status='PENDING', created_date__lte=timezone.now())
            progressing_tasks = Task.objects.filter(user=user.user, status='IN_PROGRESS', created_date__lte=timezone.now())
            completed_tasks = Task.objects.filter(user=user.user, status='COMPLETED', created_date__lte=timezone.now())
            cancelled_tasks = Task.objects.filter(user=user.user, status='CANCELLED', created_date__lte=timezone.now())
            message = f"Hey, {user.user.username}\n    Here is your detailed summary of past 24 hours:\n"
            pending_tasks_str = "Pending Tasks:\n"
            for idx, pending_task in enumerate(pending_tasks):
                pending_tasks_str += f"{idx + 1}. {pending_task.title}\n"
            progressing_tasks_str = "Progressing Tasks:\n"
            for idx, progressing_task in enumerate(progressing_tasks):
                progressing_tasks_str += f"{idx + 1}. {progressing_task.title}\n"
            completed_tasks_str = "Completed Tasks:\n"
            for idx, completed_task in enumerate(completed_tasks):
                completed_tasks_str += f"{idx + 1}. {completed_task.title}\n"
            cancelled_tasks_str = "Cancelled Tasks:\n"
            for idx, cancelled_task in enumerate(cancelled_tasks):
                cancelled_tasks_str += f"{idx + 1}. {cancelled_task.title}\n"
            
            complete_line = "\n" + "="*30 + "\n"
            message = message + '\n' + pending_tasks_str + complete_line + progressing_tasks_str + \
                complete_line + completed_tasks_str + complete_line + cancelled_tasks_str
            send_mail('Your 24 hours Tasks Summary', message, 'marmik@thedataboy.com', [user.user.email])
