import datetime
import time
from contextlib import contextmanager
from hashlib import md5

from celery.decorators import periodic_task
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from task_manager.celery import app

from .models import STATUS_CHOICES, Task, UserTaskReportSetting

LOCK_EXPIRE = 60 * 60 * 24

@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            cache.delete(lock_id)


@periodic_task(run_every=datetime.timedelta(minutes=1), bind=True)
def send_email_reports(*args, **kwargs):
    for user_setting in UserTaskReportSetting.objects.all():
        k_start = datetime.datetime.now().replace(tzinfo=None)
        k_end = datetime.datetime.combine(datetime.datetime.now().date(), user_setting.report_time, tzinfo=None)
        k = (k_end - k_start).total_seconds()
        print("total seconds:", k)
        if k < 60 and k_start < k_end:
            user_id_hexdigest = md5(str(user_setting.id).encode('utf-8')).hexdigest()
            with memcache_lock(user_id_hexdigest, app.oid) as acquired:
                if acquired:
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
