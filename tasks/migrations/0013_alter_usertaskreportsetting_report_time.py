# Generated by Django 4.0.1 on 2022-01-28 15:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_alter_usertaskreportsetting_report_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertaskreportsetting',
            name='report_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]