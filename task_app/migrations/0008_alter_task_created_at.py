# Generated by Django 3.2 on 2021-04-28 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0007_auto_20210428_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]