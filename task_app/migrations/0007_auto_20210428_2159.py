# Generated by Django 3.2 on 2021-04-28 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0006_auto_20210428_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_at_timestamp',
            field=models.FloatField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline_timestamp',
            field=models.FloatField(editable=False, null=True),
        ),
    ]
