# Generated by Django 3.2 on 2021-04-28 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0003_alter_task_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='deadline_timestamp',
            field=models.FloatField(default=1619542392.0, editable=False),
        ),
    ]
