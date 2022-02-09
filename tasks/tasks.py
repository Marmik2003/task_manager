import datetime
import time

from celery.decorators import periodic_task
from django.db import transaction
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone
from task_manager.celery import app

from .models import STATUS_CHOICES, Task, UserTaskReportSetting


@periodic_task(run_every=datetime.timedelta(minutes=1), bind=True)
def send_email_reports(*args, **kwargs):
    timeframe = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=1)
    tasks_settings = UserTaskReportSetting.objects.select_for_update().filter(
        Q(last_sent_at__isnull=True) | Q(last_sent_at__lt=timeframe)
    )
    with transaction.atomic():
        for user_setting in tasks_settings:
            complete_line = "\n" + "="*30 + "\n\n"
            message = f"Hey, {user_setting.user.username}\n    Here is your detailed summary of past 24 hours:\n\n"
            for status_val, status_text in STATUS_CHOICES:
                status_str = f"{status_text} Tasks:\n"
                message += status_str
                tasks = Task.objects.filter(user=user_setting.user, status=status_val)
                if tasks.count() != 0:
                    for idx, task in enumerate(tasks):
                        message += f"{idx+1}. {task.title}\n"
                else:
                    message += "Nothing to show!\n"
                message += complete_line
            send_mail('Your 24 hours Tasks Summary', message, 'marmik@thedataboy.com', [user_setting.user.email])
            user_setting.last_sent_at = datetime.datetime.now(timezone.utc).replace(hour=user_setting.report_time.hour, minute=user_setting.report_time.minute)
            user_setting.save()
    return tasks_settings.count()
