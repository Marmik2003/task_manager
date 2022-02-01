# Generated by Django 4.0.1 on 2022-01-28 14:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0009_remove_task_completed_remove_taskhistory_completed_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTaskReportSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_time', models.TimeField(default=datetime.time(14, 59, 30, 221653))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
    ]