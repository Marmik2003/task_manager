# Generated by Django 4.0.1 on 2022-01-26 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_taskhistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskhistory',
            old_name='created_date',
            new_name='changed_at',
        ),
    ]
