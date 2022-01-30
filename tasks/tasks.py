from .models import UserTaskReportSetting, Task, STATUS_CHOICES
import datetime
from django.utils import timezone
from celery.decorators import periodic_task
from task_manager.celery import app

from django.core.mail import send_mail


@periodic_task(run_every=datetime.timedelta(minutes=1), ignore_result=False)
def send_email_reports():
    user_send_email.delay()


@app.task(ignore_result=True)
def user_send_email():
    for user_setting in UserTaskReportSetting.objects.all():
        k_start = timezone.now().replace(tzinfo=None)
        k_end = datetime.datetime.combine(timezone.now().date(), user_setting.report_time, tzinfo=None)
        k = (k_end - k_start).total_seconds()
        if k < 60:
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
